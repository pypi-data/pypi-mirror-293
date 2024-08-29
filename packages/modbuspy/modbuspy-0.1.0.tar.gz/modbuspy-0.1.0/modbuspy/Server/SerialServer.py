import asyncio
import struct
from typing import Dict, Optional

import serial_asyncio
import yaml

from modbuspy import (
    READ_COIL,
    READ_DISCRETE_INPUT,
    READ_HOLDING_REGISTER,
    READ_INPUT_REGISTER,
    WRITE_MULTIPLE_COILS,
    WRITE_MULTIPLE_REGISTERS,
    WRITE_SINGLE_COIL,
    WRITE_SINGLE_REGISTER,
    logger,
)
from modbuspy.ADU.SerialADU import SerialADU
from modbuspy.ADU.TCPADU import TCPADU
from modbuspy.PDU.ServerPDU import (
    PDUErrorResponse,
    PDUReadResponse,
    PDUWriteMultipleResponse,
    PDUWriteSingleResponse,
)
from modbuspy.Server import Server

from modbuspy.Server.Slave import Slave


class SerialServer(Server):
    def __init__(
        self,
        port: str,
        baudrate: int = 9600,
        bytesize: int = 8,
        parity: str = "N",
        stopbits: int = 1,
        timeout: float = 1.0,
    ) -> None:
        """
        Initializes the SerialServer.

        Args:
            port (str): The serial port to use.
            baudrate (int, optional): The baud rate. Defaults to 9600.
            bytesize (int, optional): The byte size. Defaults to 8.
            parity (str, optional): The parity. Defaults to 'N'.
            stopbits (int, optional): The stop bits. Defaults to 1.
            timeout (float, optional): The timeout in seconds. Defaults to 1.0.
        """
        super().__init__()
        self.port: str = port
        self.baudrate: int = baudrate
        self.bytesize: int = bytesize
        self.parity: str = parity
        self.stopbits: int = stopbits
        self.timeout: float = timeout
        self._unit_id: int | None = None

    async def start(self):
        """
        Starts the Serial server.
        """
        reader, writer = await serial_asyncio.open_serial_connection(
            url=self.port,
            baudrate=self.baudrate,
            bytesize=self.bytesize,
            parity=self.parity,
            stopbits=self.stopbits,
        )

        while True:
            await self.handle_connection(reader, writer)

    async def parse_adu(self, data: bytes) -> SerialADU:
        serial_adu = SerialADU()
        serial_adu.from_bytes(data)
        self._unit_id = serial_adu.unit_id
        return serial_adu

    async def pack_adu(
        self,
        pdu: (
            PDUErrorResponse
            | PDUReadResponse
            | PDUWriteSingleResponse
            | PDUWriteMultipleResponse
        ),
    ) -> SerialADU:
        serial_adu = SerialADU(self._unit_id, pdu.to_bytes())
        return serial_adu
