import asyncio

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
from modbuspy.PDU.ServerPDU import (
    PDUErrorResponse,
    PDUReadResponse,
    PDUWriteMultipleResponse,
    PDUWriteSingleResponse,
)
from modbuspy.Server.Slave import Slave

from abc import ABC, abstractmethod


class Server(ABC):
    def __init__(self):
        """Initializes the Server with an empty dictionary of slaves and an asyncio lock."""
        self.slaves: dict[int, Slave] = {}
        self.lock = asyncio.Lock()

    @abstractmethod
    async def start(self):
        """Starts the server. This method should be implemented by subclasses."""
        pass

    async def add_slave(self, unit_id: int):
        """Adds a slave to the server.

        Args:
            unit_id (int): The unit ID of the slave to add.
        """
        async with self.lock:
            self.slaves[unit_id] = Slave()

    async def delete_slave(self, unit_id: int):
        """Deletes a slave from the server.

        Args:
            unit_id (int): The unit ID of the slave to delete.
        """
        async with self.lock:
            del self.slaves[unit_id]

    async def handle_connection(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ):
        """Handles an incoming connection, reading and processing data."""
        try:
            while True:
                data = await reader.read(512)
                if not data:
                    break
                adu = await self.parse_adu(data)
                response_pdu = await self.process_pdu(adu)
                response_adu = await self.pack_adu(response_pdu)
                writer.write(response_adu.to_bytes())
                await writer.drain()
        except Exception as e:
            logger.error(f"Connection error: {e}")
        finally:
            writer.close()
            await writer.wait_closed()
            reader.feed_eof()

    @abstractmethod
    async def parse_adu(self, data: bytes) -> TCPADU | SerialADU:
        """Parses the Application Data Unit (ADU).

        Args:
            data (bytes): The raw data to parse.

        Returns:
            TCPADU | SerialADU: The parsed ADU.
        """
        pass

    @abstractmethod
    async def pack_adu(
        self,
        pdu: (
            PDUErrorResponse
            | PDUReadResponse
            | PDUWriteSingleResponse
            | PDUWriteMultipleResponse
        ),
    ) -> TCPADU | SerialADU:
        """Packs the Protocol Data Unit (PDU) into an ADU.

        Args:
            pdu (PDUErrorResponse | PDUReadResponse | PDUWriteSingleResponse | PDUWriteMultipleResponse): The PDU to pack.

        Returns:
            TCPADU | SerialADU: The packed ADU.
        """
        pass

    async def process_pdu(
        self, adu: TCPADU | SerialADU
    ) -> (
        PDUReadResponse
        | PDUWriteSingleResponse
        | PDUWriteMultipleResponse
        | PDUErrorResponse
    ):
        """Processes the PDU from the ADU.

        Args:
            adu (TCPADU | SerialADU): The ADU containing the PDU to process.

        Returns:
            PDUReadResponse | PDUWriteSingleResponse | PDUWriteMultipleResponse | PDUErrorResponse: The response PDU.
        """
        try:
            slave = self.slaves[adu.unit_id]
        except KeyError:
            logger.error(f"Slave {adu.unit_id} not found")
            return PDUErrorResponse(function_code=adu.pdu[0], error_code=0x04)
        function_code = adu.pdu[0]
        if function_code == READ_COIL:
            logger.debug(f"Server received read coils request: {adu.pdu}")
            try:
                pdu = PDUReadCoils()
                pdu.from_bytes(adu.pdu)
                return await self.handle_read_coils(slave, pdu)
            except Exception as e:
                logger.error(f"Failed to handle read coils request: {e}")
                return PDUErrorResponse(function_code=adu.pdu[0], error_code=0x01)
        elif function_code == READ_DISCRETE_INPUT:
            logger.debug(f"Server received read discrete inputs request: {adu.pdu}")
            try:
                pdu = PDUReadDiscreteInputs()
                pdu.from_bytes(adu.pdu)
                return await self.handle_read_discrete_inputs(slave, pdu)
            except Exception as e:
                logger.error(f"Failed to handle read discrete inputs request: {e}")
                return PDUErrorResponse(function_code=adu.pdu[0], error_code=0x01)
        elif function_code == READ_HOLDING_REGISTER:
            logger.debug(f"Server received read holding registers request: {adu.pdu}")
            try:
                pdu = PDUReadHoldingRegisters()
                pdu.from_bytes(adu.pdu)
                return await self.handle_read_holding_registers(slave, pdu)
            except Exception as e:
                logger.error(f"Failed to handle read holding registers request: {e}")
                return PDUErrorResponse(function_code=adu.pdu[0], error_code=0x01)
        elif function_code == READ_INPUT_REGISTER:
            logger.debug(f"Server received read input registers request: {adu.pdu}")
            try:
                pdu = PDUReadInputRegisters()
                pdu.from_bytes(adu.pdu)
                return await self.handle_read_input_registers(slave, pdu)
            except Exception as e:
                logger.error(f"Failed to handle read input registers request: {e}")
                return PDUErrorResponse(function_code=adu.pdu[0], error_code=0x01)
        elif function_code == WRITE_SINGLE_COIL:
            logger.debug(f"Server received write single coil request: {adu.pdu}")
            try:
                pdu = PDUWriteSingleCoil()
                pdu.from_bytes(adu.pdu)
                return await self.handle_write_single_coil(slave, pdu)
            except Exception as e:
                logger.error(f"Failed to handle write single coil request: {e}")
                return PDUErrorResponse(function_code=adu.pdu[0], error_code=0x01)
        elif function_code == WRITE_SINGLE_REGISTER:
            logger.debug(f"Server received write single register request: {adu.pdu}")
            try:
                pdu = PDUWriteSingleRegister()
                pdu.from_bytes(adu.pdu)
                return await self.handle_write_single_register(slave, pdu)
            except Exception as e:
                logger.error(f"Failed to handle write single register request: {e}")
                return PDUErrorResponse(function_code=adu.pdu[0], error_code=0x01)
        elif function_code == WRITE_MULTIPLE_COILS:
            logger.debug(f"Server received write multiple coils request: {adu.pdu}")
            try:
                pdu = PDUWriteMultipleCoils()
                pdu.from_bytes(adu.pdu)
                return await self.handle_write_multiple_coils(slave, pdu)
            except Exception as e:
                logger.error(f"Failed to handle write multiple coils request: {e}")
                return PDUErrorResponse(function_code=adu.pdu[0], error_code=0x01)
        elif function_code == WRITE_MULTIPLE_REGISTERS:
            logger.debug(f"Server received write multiple registers request: {adu.pdu}")
            try:
                pdu = PDUWriteMultipleRegisters()
                pdu.from_bytes(adu.pdu)
                return await self.handle_write_multiple_registers(slave, pdu)
            except Exception as e:
                logger.error(f"Failed to handle write multiple registers request: {e}")
                return PDUErrorResponse(function_code=adu.pdu[0], error_code=0x01)
        else:
            logger.error(f"Unsupported function code: {function_code}")
            return PDUErrorResponse(function_code=adu.pdu[0], error_code=0x01)

    async def handle_read_coils(
        self, slave: Slave, pdu: PDUReadCoils
    ) -> PDUReadResponse | PDUErrorResponse:
        """Handles a read coils request.

        Args:
            slave (Slave): The slave to read from.
            pdu (PDUReadCoils): The PDU containing the read coils request.

        Returns:
            PDUReadResponse | PDUErrorResponse: The response PDU.
        """

        def serialize_coils(values: list[bool]) -> bytes:
            byte_count = (len(values) + 7) // 8
            coil_data = bytearray(byte_count)

            for i, value in enumerate(values):
                if value:
                    coil_data[i // 8] |= 1 << (i % 8)

            return bytes(coil_data)

        coils = []
        for i in range(pdu.quantity):
            address = pdu.starting_address + i
            if address not in slave.coils:
                return PDUErrorResponse(
                    function_code=pdu.function_code, error_code=0x02
                )
            coils.append(slave.coils[address].value)
        serialized_coils = serialize_coils(coils)
        response_pdu = PDUReadResponse(function_code=pdu.function_code, data=serialized_coils)
        logger.debug(f"Server sent read coils response: {response_pdu.to_bytes()}")
        return response_pdu

    async def handle_read_discrete_inputs(
        self, slave: Slave, pdu: PDUReadDiscreteInputs
    ) -> PDUReadResponse | PDUErrorResponse:
        """Handles a read discrete inputs request.

        Args:
            slave (Slave): The slave to read from.
            pdu (PDUReadDiscreteInputs): The PDU containing the read discrete inputs request.

        Returns:
            PDUReadResponse | PDUErrorResponse: The response PDU.
        """

        def serialize_discrete_inputs(values: list[bool]) -> bytes:
            byte_count = (len(values) + 7) // 8
            discrete_input_data = bytearray(byte_count)

            for i, value in enumerate(values):
                if value:
                    discrete_input_data[i // 8] |= 1 << (i % 8)

            return bytes(discrete_input_data)

        discrete_inputs = []
        for i in range(pdu.quantity):
            address = pdu.starting_address + i
            if address not in slave.discrete_inputs:
                return PDUErrorResponse(
                    function_code=pdu.function_code, error_code=0x02
                )
            discrete_inputs.append(slave.discrete_inputs[address].value)
        serialized_discrete_inputs = serialize_discrete_inputs(discrete_inputs)
        response_pdu = PDUReadResponse(
            function_code=pdu.function_code, data=serialized_discrete_inputs
        )
        logger.debug(f"Server sent read discrete inputs response: {response_pdu.to_bytes()}")
        return response_pdu

    async def handle_read_holding_registers(
        self, slave: Slave, pdu: PDUReadHoldingRegisters
    ) -> PDUReadResponse | PDUErrorResponse:
        """Handles a read holding registers request.

        Args:
            slave (Slave): The slave to read from.
            pdu (PDUReadHoldingRegisters): The PDU containing the read holding registers request.

        Returns:
            PDUReadResponse | PDUErrorResponse: The response PDU.
        """

        def serialize_holding_registers(values: list[bytes]) -> bytes:
            return b"".join(values)

        holding_registers = []
        for i in range(pdu.quantity):
            address = pdu.starting_address + i
            if address not in slave.holding_registers:
                return PDUErrorResponse(
                    function_code=pdu.function_code, error_code=0x02
                )
            holding_registers.append(slave.holding_registers[address].value)

        serialized_holding_registers = serialize_holding_registers(holding_registers)
        response_pdu = PDUReadResponse(
            function_code=pdu.function_code, data=serialized_holding_registers
        )
        logger.debug(f"Server sent read holding registers response: {response_pdu.to_bytes()}")
        return response_pdu

    async def handle_read_input_registers(
        self, slave: Slave, pdu: PDUReadInputRegisters
    ) -> PDUReadResponse | PDUErrorResponse:
        """Handles a read input registers request.

        Args:
            slave (Slave): The slave to read from.
            pdu (PDUReadInputRegisters): The PDU containing the read input registers request.

        Returns:
            PDUReadResponse | PDUErrorResponse: The response PDU.
        """

        def serialize_input_registers(values: list[bytes]) -> bytes:
            return b"".join(values)

        input_registers = []
        for i in range(pdu.quantity):
            address = pdu.starting_address + i
            if address not in slave.input_registers:
                return PDUErrorResponse(
                    function_code=pdu.function_code, error_code=0x02
                )
            input_registers.append(slave.input_registers[address].value)

        serialized_input_registers = serialize_input_registers(input_registers)
        response_pdu = PDUReadResponse(
            function_code=pdu.function_code, data=serialized_input_registers
        )
        logger.debug(f"Server sent read input registers response: {response_pdu.to_bytes()}")
        return response_pdu

    async def handle_write_single_coil(
        self, slave: Slave, pdu: PDUWriteSingleCoil
    ) -> PDUErrorResponse | PDUWriteSingleResponse:
        """Handles a write single coil request.

        Args:
            slave (Slave): The slave to write to.
            pdu (PDUWriteSingleCoil): The PDU containing the write single coil request.

        Returns:
            PDUErrorResponse | PDUWriteSingleResponse: The response PDU.
        """
        address = pdu.address
        if address not in slave.coils:
            return PDUErrorResponse(function_code=pdu.function_code, error_code=0x02)
        slave.coils[address].value = pdu.value
        response_pdu = PDUWriteSingleResponse(
            function_code=pdu.function_code,
            address=address,
            value=b"\xff\x00" if pdu.value else b"\x00\x00",
        )
        logger.debug(f"Server sent write single coil response: {response_pdu.to_bytes()}")
        return response_pdu

    async def handle_write_single_register(
        self, slave: Slave, pdu: PDUWriteSingleRegister
    ) -> PDUErrorResponse | PDUWriteSingleResponse:
        """Handles a write single register request.

        Args:
            slave (Slave): The slave to write to.
            pdu (PDUWriteSingleRegister): The PDU containing the write single register request.

        Returns:
            PDUErrorResponse | PDUWriteSingleResponse: The response PDU.
        """
        address = pdu.address
        if address not in slave.holding_registers:
            return PDUErrorResponse(function_code=pdu.function_code, error_code=0x02)
        slave.holding_registers[address].value = pdu.value
        response_pdu = PDUWriteSingleResponse(function_code=pdu.function_code, address=address, value=slave.holding_registers[address].value)
        logger.debug(f"Server sent write single register response: {response_pdu.to_bytes()}")
        return response_pdu

    async def handle_write_multiple_coils(
        self, slave: Slave, pdu: PDUWriteMultipleCoils
    ) -> PDUErrorResponse | PDUWriteMultipleResponse:
        """Handles a write multiple coils request.

        Args:
            slave (Slave): The slave to write to.
            pdu (PDUWriteMultipleCoils): The PDU containing the write multiple coils request.

        Returns:
            PDUErrorResponse | PDUWriteMultipleResponse: The response PDU.
        """
        for i, value in enumerate(pdu.values):
            address = pdu.starting_address + i
            if address not in slave.coils:
                return PDUErrorResponse(
                    function_code=pdu.function_code, error_code=0x02
                )
            slave.coils[address].value = value
        response_pdu = PDUWriteMultipleResponse(function_code=pdu.function_code, starting_address=pdu.starting_address, quantity=len(pdu.values))
        logger.debug(f"Server sent write multiple coils response: {response_pdu.to_bytes()}")
        return response_pdu

    async def handle_write_multiple_registers(
        self, slave: Slave, pdu: PDUWriteMultipleRegisters
    ) -> PDUErrorResponse | PDUWriteMultipleResponse:
        """Handles a write multiple registers request.

        Args:
            slave (Slave): The slave to write to.
            pdu (PDUWriteMultipleRegisters): The PDU containing the write multiple registers request.

        Returns:
            PDUErrorResponse | PDUWriteMultipleResponse: The response PDU.
        """
        for i, value in enumerate(pdu.values):
            address = pdu.starting_address + i
            if address not in slave.holding_registers:
                return PDUErrorResponse(
                    function_code=pdu.function_code, error_code=0x02
                )
            slave.holding_registers[address].value = value
        response_pdu = PDUWriteMultipleResponse(function_code=pdu.function_code, starting_address=pdu.starting_address, quantity=len(pdu.values))
        logger.debug(f"Server sent write multiple registers response: {response_pdu.to_bytes()}")
        return response_pdu
