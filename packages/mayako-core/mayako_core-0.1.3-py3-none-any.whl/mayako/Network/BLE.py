from bleak import BleakClient
import asyncio
from queue import Queue
import threading
from typing import Optional

from .NetworkInterface import NetworkInterface
from ..Config import CNETWORK, CPACKET
from .Packet import Packet

class BLE(NetworkInterface):
    """
    Source
        https://www.instructables.com/Starting-and-Stopping-Python-Threads-With-Events-i/
        https://stackoverflow.com/a/68121144
        https://docs.python.org/3/library/asyncio-eventloop.html
        https://stackoverflow.com/a/71489745
    """
    _characteristic: str
    _timeout: int
    _client: BleakClient
    _read_queue: Queue[Packet]
    _write_queue: Queue[Packet]
    _loop: asyncio.AbstractEventLoop
    _thread: threading.Thread
    _connected: bool

#TODO: on disconnect, try reconnect directly; maybe we can avoid hicubs like this#
#reconnect if the number of clients defined are reduced?

#TODO: callback disconnect => connected = false
    def __init__(self, address: str, characteristic: str, timeout: int = CNETWORK.TIMEOUT) -> None:
        self._characteristic = characteristic
        self._timeout = timeout
        self._client = BleakClient(address, timeout=self._timeout)
        self._read_queue = Queue()
        self._write_queue = Queue()
        self._loop = asyncio.new_event_loop()
        self._thread = None
        self._connected = False

    def connect(self) -> None:
        if self._thread and self._thread.is_alive():
            #TODO log warning that the thread was still alive
            self._thread.join()

        self._thread = threading.Thread(target=self._handle_device)
        self._thread.start()
    
    #TODO: ble callback disconnect/connect?!

    async def _handle_device(self) -> None:
        try:
            await self._connect_client()

            if self._connected:
                notify_task = self._loop.create_task(self._start_notify())
                write_task = self._loop.create_task(self._write_data())

                await asyncio.gather(notify_task, write_task)

        except asyncio.CancelledError:
            #TODO logging
            pass
        finally:
            await self._stop_notify()
            await self._client.disconnect()

    async def _connect_client(self) -> None:
        try:
            await self._client.connect()
            self._connected = self._client.is_connected
        except Exception as e:
            #TODO: log exception
            self._connected = False
            
    async def _start_notify(self):
        try:
            await self._client.start_notify(self._characteristic, self._notification_handler)
        except Exception as e:
            #TODO logging
            pass

    async def _stop_notify(self):
        try:
            await self._client.stop_notify(self._characteristic)
        except Exception as e:
            #TODO logging
            pass

    def _notification_handler(self, sender: str, data: bytes):
        #TODO: update from m5-test: ble.py so that we can read chunks
        if len(data) < CPACKET.HEADER_SIZE:
            #not enough data to process
            #LOGGING
            return
        
        index = 0

        while index + CPACKET.HEADER_SIZE <= len(data):
            first_byte = data[index]

            if not Packet.verify_flag(first_byte):
                index += 1
                continue #move to next byte and check if this is the flag
        
            packet = Packet()

            header_data = data[index:index + CPACKET.HEADER_SIZE]
            packet.deserialize_header(header_data)

            payload_start = index + CPACKET.HEADER_SIZE
            payload_stop =  payload_start + packet.get_payload_size()

            if len(data) < payload_stop:
                break #not enough data for payload, so we completly trash the packet
                #TODO: i guess we should logg this for a while to see if the MTU make a problem?!

            payload_data = data[payload_start : payload_stop]
            packet.deserialize_payload(payload_data)

            self._read_queue.put(packet)

            break

    async def _write_data(self) -> None:
        while self._connected:
            if not self._write_queue.empty():
                packet = self._write_queue.get()
                serialised_data = packet.serialize()

                try:
                    await self._client.write_gatt_char(self._characteristic, serialised_data)
                except Exception as e:
                    # TODO: Add logging or handling for successful write
                    pass

            await asyncio.sleep(CNETWORK.BUSY_WAITING_TIMEOUT)

    def disconnect(self) -> None:
        if self._thread and self._thread.is_alive():
            self._thread.join()
        
        if self._loop.is_running():
            self._loop.run_until_complete(self._loop.shutdown_asyncgens())
            self._loop.stop()

        self._loop.close()

        #TODO: logging

        self._connected = False

    def write(self, data: Packet) -> None:
        self._write_queue.put(data)

    def read(self) -> Optional[Packet]:
        if self._read_queue.qsize() > 0:
            return self._read_queue.get()

        return None

    def check_connection(self) -> bool:
        return self._connected
    