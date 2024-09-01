"""Serving data over http."""
import asyncio
import atexit
import logging
import sqlite3
from datetime import datetime
from multiprocessing import Process
from pathlib import Path
from typing import Any, Awaitable

import websockets

from dojo.data.protobuf.dashboard.v1.data_pb2 import (
    AgentParams,
    Block,
    BlockData,
    ClientData,
    FileChunk,
    Params,
    Pool,
    ServerData,
)

logger = logging.getLogger(__name__)

SEND_EVERY = 2


class _ClientDataProvider:
    def __init__(self, start_block: int, end_block: int, db_path: Path, port: int):
        self.start_block = start_block
        self.end_block = end_block
        self.db_path = db_path
        self.port = port
        self.connected_clients = set()
        self.clients_waiting_to_save = set()
        self.is_dojo_process_running = False
        self.stop_event = asyncio.Event()
        self.start_time = datetime.now()

    def start(self) -> None:
        # TODO: use process groups to make sure signals are distributed to all sub processes, so that if
        # we receive a SIGKILL then we can still halt properly.
        self.toggle_dojo_process_running(True)
        self.process = Process(target=self.start_websocket_server)
        self.process.start()
        atexit.register(self.stop)

    def stop(self) -> None:
        self.stop_event.set()
        self.process.kill()

    def toggle_dojo_process_running(self, is_running) -> bool:
        self.is_dojo_process_running = is_running

    def start_websocket_server(self) -> None:
        async def main(port):
            logger.info("Running ClientDataProvider socket on PORT %s", port)
            async with websockets.serve(self.websocket_handler, "", port):
                await self.stop_event.wait()  # Wait for the stop event

        asyncio.run(main(self.port), debug=False)

    async def websocket_handler(self, websocket) -> Awaitable[None]:
        try:
            # Listen for client websocket messages
            async for message in websocket:
                try:
                    client_data = ClientData()
                    client_data.ParseFromString(message)

                    # Receiving a message from client with last_block_num_processed key confirms it is dashboard
                    # attempting to onboard
                    if client_data.last_block_num_processed or client_data.all_blocks:
                        await self.onboard_client(
                            websocket, client_data.last_block_num_processed or None
                        )

                    # Receiving message with save_data key indicates they would like db file sent
                    # at end of Dojo process
                    elif client_data.save.save_data:
                        if self.is_dojo_process_running:
                            # send after dojo has finished it's process

                            self.clients_waiting_to_save.add(
                                (
                                    websocket,
                                    client_data.save.title,
                                    client_data.save.description,
                                )
                            )
                        else:
                            # send right away
                            await self.send_database_file_to_clients(
                                set(
                                    [
                                        (
                                            websocket,
                                            client_data.save.title,
                                            client_data.save.description,
                                        )
                                    ]
                                )
                            )
                    elif not client_data.save.save_data:
                        self.clients_waiting_to_save.remove(websocket)
                except:  # noqa: E722
                    # If websocket client connects and sends a message with fields other than what we're expecting
                    # Confirms we do not want to add this client to our set of dashboard clients
                    logger.error(
                        "Client websocket other than Dojo dashboard tried to connect and send a message"
                    )

        except websockets.ConnectionClosed:
            logger.debug("Client disconnected")
            self.connected_clients.remove(websocket)
            self.clients_waiting_to_save.remove(websocket)

    async def run_data_sender_loop(self, last_block_id) -> Awaitable[None]:
        # Run only if there are connected clients and no asyncio stop event
        while self.connected_clients and not self.stop_event.is_set():
            # Loop looks for new data every 2 sec
            await asyncio.sleep(SEND_EVERY)

            new_block_data = self.get_block_data(last_block_id)
            if new_block_data:
                data, last_block_id = self.format_data(
                    new_block_data, last_block_id=last_block_id
                )
                await asyncio.gather(
                    *[
                        client.send(data.SerializeToString())
                        for client in self.connected_clients
                    ]
                )

            if not self.is_dojo_process_running:
                break

        if (
            self.clients_waiting_to_save
        ):  # TODO Should 'not self.stop_event.is_set()' be set here?

            await self.send_database_file_to_clients(self.clients_waiting_to_save)

    async def send_database_file_to_clients(self, clients) -> Awaitable[None]:

        # chunk_size = 1024  # 1KB chunks
        # sequence_number = 1

        with open(self.db_path, "rb") as f:
            for client in clients:
                server_data = ServerData()
                server_data.file_chunk.CopyFrom(
                    FileChunk(data=f.read(), title=client[1], description=client[2])
                )
                # Serialize the protobuf message
                serialized_data = server_data.SerializeToString()
                await client[0].send(serialized_data)

        # await asyncio.gather(
        #     *[
        #         client[0].send(serialized_data)
        #         for client in clients
        #     ]
        # )
        # await websocket.send(serialized_data)

        # with open(self.db_path, "rb") as file:
        #     while True:
        #         chunk = file.read(chunk_size)  # Read in 1KB chunks
        #         if not chunk:
        #             break

        #         data = Data()
        #         data.file_chunk.CopyFrom(
        #             FileChunk(
        #                 data=chunk,
        #                 sequence_number=sequence_number,
        #                 is_last_chunk=False
        #             )
        #         )
        #         print(f"sending chunk {sequence_number}")
        #         await asyncio.gather(
        #             *[
        #                 client.send(data.SerializeToString())
        #                 for client in clients
        #             ]
        #         )
        #         sequence_number += 1

        #     # Send a final chunk to indicate the end of the file
        #     data = Data()
        #     data.file_chunk.CopyFrom(
        #         FileChunk(
        #             data=b'',
        #             sequence_number=sequence_number,
        #             is_last_chunk=True
        #         )
        #     )
        #     print(f"sending final chunk {sequence_number}")
        #     await asyncio.gather(
        #         *[
        #             client.send(data.SerializeToString())
        #             for client in clients
        #         ]
        #     )

    async def onboard_client(self, websocket, last_block_id) -> Awaitable[None]:
        self.connected_clients.add(websocket)
        params = self.get_params()
        agents = self.get_agents()
        pools = self.get_pools()
        all_block_data = self.get_block_data(last_block_id)

        # Send all data to the newly connected client
        data, last_block_id = self.format_data(
            all_block_data,
            last_block_id=last_block_id,
            params=params,
            agents=agents,
            pools=pools,
        )
        await websocket.send(data.SerializeToString())

        # Start data sending loop when the first client connects
        if len(self.connected_clients) == 1:
            asyncio.create_task(self.run_data_sender_loop(last_block_id))

    def format_data(
        self, block_data, last_block_id=None, params=None, agents=None, pools=None
    ) -> Any:
        server_data = ServerData()

        if params:
            server_data.params.CopyFrom(
                Params(
                    environment=params[0],
                    start_date=params[1],
                    end_date=params[2],
                    start_block=params[3],
                    end_block=params[4],
                )
            )

        if agents:
            for agent in agents:
                server_data.params.agents.append(
                    AgentParams(address=agent[0], name=agent[1])
                )
        if pools:
            for pool in pools:
                server_data.params.pools.append(
                    Pool(name=pool[0], token0=pool[1], token1=pool[2], fee=pool[3])
                )

        for row in block_data:
            # will equal the final processed row id
            last_block_id = row[0]

            # Deserialize the message from the string
            block_data = BlockData()
            block_data.ParseFromString(row[1])

            # assign repeated Block message to Data Message
            block = Block(block_num=row[0], block_data=block_data)
            server_data.block_data_list.append(block)

        # add progress percentage relative to last block processed
        progress = self.get_progress(last_block_id)

        server_data.progress = progress
        seconds_remaining = self.get_estimated_seconds_remaining(progress)
        if seconds_remaining:
            server_data.estimatedSecondsRemaining = seconds_remaining
        if last_block_id:
            server_data.last_block_num_processed = last_block_id

        return server_data, last_block_id

    def get_params(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT environment, start_date, end_date, start_block, end_block FROM params"
        )
        row = cursor.fetchone()
        return row

    def get_agents(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT address, name FROM agents")
        rows = cursor.fetchall()
        return rows

    def get_pools(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name, token0, token1, fee FROM pools")
        rows = cursor.fetchall()
        return rows

    def get_block_data(self, last_block_id=None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        columns_to_query = """
            block,
            protobuf_serialized_data,
            timestamp
        """
        if last_block_id:
            cursor.execute(
                f"""
                SELECT {columns_to_query} FROM blockdata WHERE block > ? ORDER BY timestamp ASC
                """,
                (last_block_id,),
            )
        else:
            cursor.execute(
                f"""
                SELECT {columns_to_query} FROM blockdata ORDER BY timestamp ASC
                """
            )

        rows = cursor.fetchall()
        conn.close()
        return rows

    def get_progress(self, block):
        progress = 0
        if block:
            progress = round(
                (block - self.start_block) * 100 / (self.end_block - self.start_block),
                2,
            )
        return progress

    def get_estimated_seconds_remaining(self, progress):
        if progress == 0:
            return None
        progress = progress / 100
        now = datetime.now()
        time_difference = now - self.start_time
        total_time = int(time_difference.seconds / progress)
        return total_time - time_difference.seconds
