import asyncio
import ssl

from typing import Optional

from modbuspy import logger
from modbuspy.ADU.TCPADU import TCPADU
from modbuspy.PDU.ClientPDU import (
    PDUReadCoils,
    PDUReadDiscreteInputs,
    PDUReadHoldingRegisters,
    PDUReadInputRegisters,
    PDUWriteMultipleCoils,
    PDUWriteMultipleRegisters,
    PDUWriteSingleCoil,
    PDUWriteSingleRegister,
)
from modbuspy.Client import Client


class TCPClient(Client):
    def __init__(
        self,
        host: str,
        port: int,
        use_tls: bool = False,
        cert_file: Optional[str] = None,
        key_file: Optional[str] = None,
        ca_file: Optional[str] = None,
    ) -> None:
        super().__init__()
        self.host: str = host
        self.port: int = port
        self.use_tls: bool = use_tls
        self.cert_file = cert_file
        self.key_file = key_file
        self.ca_file = ca_file
        self._transaction_id: int = 0

    @property
    def transaction_id(self) -> int:
        return self._transaction_id

    @transaction_id.setter
    def transaction_id(self, value: int) -> None:
        self._transaction_id = value

    async def connect(self) -> None:
        """
        Establishes a connection to the Modbus server.
        """
        if self.use_tls:
            ssl_context = ssl.create_default_context(
                ssl.Purpose.SERVER_AUTH, cafile=self.ca_file
            )
            if self.cert_file and self.key_file:
                ssl_context.load_cert_chain(
                    certfile=self.cert_file, keyfile=self.key_file
                )
            self._reader, self._writer = await asyncio.open_connection(
                self.host, self.port, ssl=ssl_context
            )
        else:
            self._reader, self._writer = await asyncio.open_connection(
                self.host, self.port
            )

    async def close(self) -> None:
        """
        Closes the connection to the Modbus server.
        """
        if self._writer:
            self._writer.close()
            await self._writer.wait_closed()
        if self._reader:
            self._reader.feed_eof()


    async def send_request(
        self,
        unit_id: int,
        pdu: (
            PDUReadCoils
            | PDUReadDiscreteInputs
            | PDUReadHoldingRegisters
            | PDUReadInputRegisters
            | PDUWriteMultipleCoils
            | PDUWriteMultipleRegisters
            | PDUWriteSingleCoil
            | PDUWriteSingleRegister
        ),
    ) -> None:
        self.transaction_id += 1
        tcp_adu = TCPADU(self.transaction_id, unit_id, pdu.to_bytes())
        self.writer.write(tcp_adu.to_bytes())
        await self.writer.drain()
        logger.debug(f"Client sent request: {tcp_adu.to_bytes()}")

    async def read_response(self) -> TCPADU:
        adu_bytes = await self.reader.read(512)
        adu = TCPADU()
        adu.from_bytes(adu_bytes)
        logger.debug(f"Client received response: {adu.to_bytes()}")
        return adu
