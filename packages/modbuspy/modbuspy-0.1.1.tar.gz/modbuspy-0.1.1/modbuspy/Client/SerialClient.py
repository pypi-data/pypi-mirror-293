import serial_asyncio

from modbuspy import logger
from modbuspy.ADU.SerialADU import SerialADU
from modbuspy.Client import Client
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


class SerialClient(Client):
    def __init__(
        self,
        port: str,
        baudrate: int = 9600,
        bytesize: int = 8,
        parity: str = "N",
        stopbits: int = 1,
        timeout: float = 1.0,
    ) -> None:
        super().__init__()
        self.port = port
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self.timeout = timeout

    async def connect(self) -> None:
        """
        Establishes a connection to the Modbus server.
        """
        self._reader, self._writer = await serial_asyncio.open_serial_connection(
            url=self.port,
            baudrate=self.baudrate,
            bytesize=self.bytesize,
            parity=self.parity,
            stopbits=self.stopbits,
            timeout=self.timeout,
        )

    async def close(self) -> None:
        """
        Closes the connection to the Modbus server.
        """
        if self.writer:
            self.writer.close()
            await self.writer.wait_closed()
        if self.reader:
            self.reader.feed_eof()

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
        serial_adu = SerialADU(unit_id, pdu.to_bytes())
        self.writer.write(serial_adu.to_bytes())
        await self.writer.drain()
        logger.debug(f"Client sent request: {serial_adu.to_bytes()}")

    async def read_response(self) -> SerialADU:
        adu_bytes = await self.reader.read()
        adu = SerialADU()
        adu.from_bytes(adu_bytes)
        logger.debug(f"Client received response: {adu.to_bytes()}")
        return adu
