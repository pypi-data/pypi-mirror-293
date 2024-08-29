import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Literal, Optional

from modbuspy import deserialize, logger
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
    PDUReadResponse,
    PDUWriteMultipleResponse,
    PDUWriteSingleResponse,
)


class Client(ABC):
    def __init__(
        self,
        byte_order: Literal["big", "little"] = "big",
        word_order: Literal["big", "little"] = "big",
    ) -> None:
        """
        Initializes the Client.

        Args:
            byte_order (Literal["big", "little"], optional): The byte order. Defaults to "big".
            word_order (Literal["big", "little"], optional): The word order. Defaults to "big".
        """
        self._reader: asyncio.StreamReader | None = None
        self._writer: asyncio.StreamWriter | None = None
        self.byte_order = byte_order
        self.word_order = word_order

    @property
    def reader(self) -> asyncio.StreamReader:
        """
        Gets the reader.

        Returns:
            asyncio.StreamReader: The stream reader.

        Raises:
            ValueError: If the reader is not set.
        """
        if self._reader is None:
            raise ValueError("reader is not set")
        return self._reader

    @property
    def writer(self) -> asyncio.StreamWriter:
        """
        Gets the writer.

        Returns:
            asyncio.StreamWriter: The stream writer.

        Raises:
            ValueError: If the writer is not set.
        """
        if self._writer is None:
            raise ValueError("writer is not set")
        return self._writer

    @abstractmethod
    async def connect(self) -> None:
        """
        Connects to the Modbus server.
        """
        pass

    @abstractmethod
    async def close(self) -> None:
        """
        Closes the connection to the Modbus server.
        """
        pass

    @abstractmethod
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
        """
        Sends a request to the Modbus server.

        Args:
            unit_id (int): The unit ID.
            pdu (Union[PDUReadCoils, PDUReadDiscreteInputs, PDUReadHoldingRegisters, PDUReadInputRegisters, PDUWriteMultipleCoils, PDUWriteMultipleRegisters, PDUWriteSingleCoil, PDUWriteSingleRegister]): The Protocol Data Unit (PDU).
        """
        pass

    @abstractmethod
    async def read_response(self) -> TCPADU | SerialADU:
        """
        Reads a response from the Modbus server.

        Returns:
            Union[TCPADU, SerialADU]: The Application Data Unit (ADU) response.
        """
        pass

    async def read_coils(
        self, unit_id: int, starting_address: int, quantity: int
    ) -> list[bool]:
        """
        Reads coils from the Modbus server.

        Args:
            unit_id (int): The unit ID.
            starting_address (int): The starting address of the coils.
            quantity (int): The number of coils to read.

        Returns:
            list[bool]: The list of coil values.

        Raises:
            ValueError: If there is a Modbus error.
        """
        read_pdu = PDUReadCoils(starting_address, quantity)
        await self.send_request(unit_id, read_pdu)

        response = await self.read_response()
        is_error, err_msg = response.is_error()
        if is_error:
            raise ValueError(f"ModBus error: {err_msg}")

        read_response_pdu = PDUReadResponse()
        read_response_pdu.from_bytes(response.pdu)

        inputs = [
            bool(read_response_pdu.data[i // 8] & (1 << (i % 8)))
            for i in range(quantity)
        ]

        # Log received values
        logger.info(
            f"Successfully read {quantity} coils from {starting_address} to {starting_address + quantity - 1} with values: {inputs}"
        )

        return inputs

    async def read_discrete_inputs(
        self, unit_id: int, starting_address: int, quantity: int
    ) -> list[bool]:
        """
        Reads discrete inputs from the Modbus server.

        Args:
            unit_id (int): The unit ID.
            starting_address (int): The starting address of the discrete inputs.
            quantity (int): The number of discrete inputs to read.

        Returns:
            list[bool]: The list of discrete input values.

        Raises:
            ValueError: If there is a Modbus error.
        """
        read_pdu = PDUReadDiscreteInputs(starting_address, quantity)
        await self.send_request(unit_id, read_pdu)

        response = await self.read_response()
        is_error, err_msg = response.is_error()
        if is_error:
            raise ValueError(f"ModBus error: {err_msg}")

        read_response_pdu = PDUReadResponse()
        read_response_pdu.from_bytes(response.pdu)

        inputs = [
            bool(read_response_pdu.data[i // 8] & (1 << (i % 8)))
            for i in range(quantity)
        ]

        # Log received values
        logger.info(
            f"Successfully read {quantity} discrete inputs from {starting_address} to {starting_address + quantity - 1} with values: {inputs}"
        )

        return inputs

    async def read_holding_registers(
        self, unit_id: int, starting_address: int, quantity: int
    ) -> list[bytes]:
        """
        Reads holding registers from the Modbus server.

        Args:
            unit_id (int): The unit ID.
            starting_address (int): The starting address of the holding registers.
            quantity (int): The number of holding registers to read.

        Returns:
            list[bytes]: The list of holding register values.

        Raises:
            ValueError: If there is a Modbus error.
        """
        read_pdu = PDUReadHoldingRegisters(starting_address, quantity)
        await self.send_request(unit_id, read_pdu)

        response = await self.read_response()
        is_error, err_msg = response.is_error()
        if is_error:
            raise ValueError(f"ModBus error: {err_msg}")

        read_response_pdu = PDUReadResponse()
        read_response_pdu.from_bytes(response.pdu)

        registers = [read_response_pdu.data[i * 2 : i * 2 + 2] for i in range(quantity)]
        logger.info(
            f"Successfully read {quantity} holding registers from {starting_address} to {starting_address + quantity - 1} with values: {registers}"
        )
        return registers

    async def read_input_registers(
        self, unit_id: int, starting_address: int, quantity: int
    ) -> list[bytes]:
        """
        Reads input registers from the Modbus server.

        Args:
            unit_id (int): The unit ID.
            starting_address (int): The starting address of the input registers.
            quantity (int): The number of input registers to read.

        Returns:
            list[bytes]: The list of input register values.

        Raises:
            ValueError: If there is a Modbus error.
        """
        read_pdu = PDUReadInputRegisters(starting_address, quantity)
        await self.send_request(unit_id, read_pdu)

        response = await self.read_response()
        is_error, err_msg = response.is_error()
        if is_error:
            raise ValueError(f"ModBus error: {err_msg}")

        read_response_pdu = PDUReadResponse()
        read_response_pdu.from_bytes(response.pdu)

        registers = [read_response_pdu.data[i * 2 : i * 2 + 2] for i in range(quantity)]
        logger.info(
            f"Successfully read {quantity} input registers from {starting_address} to {starting_address + quantity - 1} with values: {registers}"
        )
        return registers

    async def write_single_coil(
        self,
        unit_id: int,
        address: int,
        value: bool,
    ) -> None:
        """
        Writes a single coil to the Modbus server.

        Args:
            unit_id (int): The unit ID.
            address (int): The address of the coil.
            value (bool): The value to write.

        Raises:
            ValueError: If there is a Modbus error or an invalid response.
        """
        write_pdu = PDUWriteSingleCoil(address, value)
        await self.send_request(unit_id, write_pdu)

        response = await self.read_response()
        is_error, err_msg = response.is_error()
        if is_error:
            raise ValueError(f"ModBus error: {err_msg}")

        write_response_pdu = PDUWriteSingleResponse()
        write_response_pdu.from_bytes(response.pdu)

        if write_response_pdu.address != write_pdu.address:
            raise ValueError(
                f"invalid address in response, expect {write_pdu.address} but received {write_response_pdu.address}"
            )

        expected_value = b"\xff\x00" if write_pdu.value else b"\x00\x00"
        if write_response_pdu.value != expected_value:
            raise ValueError(
                f"invalid value in response, expect {expected_value} but received {write_response_pdu.value}"
            )

        logger.info(
            f"Successfully write single coil at {write_pdu.address} with value: {write_pdu.value}"
        )

    async def write_single_register(
        self,
        unit_id: int,
        address: int,
        value: bytes,
    ) -> None:
        """
        Writes a single register to the Modbus server.

        Args:
            unit_id (int): The unit ID.
            address (int): The address of the register.
            value (bytes): The value to write.

        Raises:
            ValueError: If there is a Modbus error or an invalid response.
        """
        write_pdu = PDUWriteSingleRegister(address, value)
        await self.send_request(unit_id, write_pdu)

        response = await self.read_response()
        is_error, err_msg = response.is_error()
        if is_error:
            raise ValueError(f"ModBus error: {err_msg}")

        write_response_pdu = PDUWriteSingleResponse()
        write_response_pdu.from_bytes(response.pdu)

        if write_response_pdu.address != write_pdu.address:
            raise ValueError(
                f"invalid address in response, expect {write_pdu.address} but received {write_response_pdu.address}"
            )

        if write_response_pdu.value != write_pdu.value:
            raise ValueError(
                f"invalid value in response, expect {write_pdu.value} but received {write_response_pdu.value}"
            )

        logger.info(
            f"Successfully write single register at {write_pdu.address} with value: {write_pdu.value}"
        )

    async def write_multiple_coils(
        self,
        unit_id: int,
        starting_address: int,
        values: list[bool],
    ) -> None:
        """
        Writes multiple coils to the Modbus server.

        Args:
            unit_id (int): The unit ID.
            starting_address (int): The starting address of the coils.
            values (list[bool]): The values to write.

        Raises:
            ValueError: If there is a Modbus error or an invalid response.
        """
        write_pdu = PDUWriteMultipleCoils(starting_address, values)
        await self.send_request(unit_id, write_pdu)

        response = await self.read_response()
        is_error, err_msg = response.is_error()
        if is_error:
            raise ValueError(f"ModBus error: {err_msg}")

        write_response_pdu = PDUWriteMultipleResponse()
        write_response_pdu.from_bytes(response.pdu)

        if write_response_pdu.starting_address != starting_address:
            raise ValueError(
                f"invalid starting address in response, expect {starting_address} but received {write_response_pdu.starting_address}"
            )

        if write_response_pdu.quantity != len(values):
            raise ValueError(
                f"invalid quantity in response, expect {len(values)} but received {write_response_pdu.quantity}"
            )

        logger.info(
            f"Successfully write multiple coils from {starting_address} to {starting_address + len(values) - 1} with values: {values}"
        )

    async def write_multiple_registers(
        self,
        unit_id: int,
        starting_address: int,
        values: list[bytes],
    ) -> None:
        """
        Writes multiple registers to the Modbus server.

        Args:
            unit_id (int): The unit ID.
            starting_address (int): The starting address of the registers.
            values (list[bytes]): The values to write.

        Raises:
            ValueError: If there is a Modbus error or an invalid response.
        """
        write_pdu = PDUWriteMultipleRegisters(starting_address, values)
        await self.send_request(unit_id, write_pdu)

        response = await self.read_response()
        is_error, err_msg = response.is_error()
        if is_error:
            raise ValueError(f"ModBus error: {err_msg}")

        write_response_pdu = PDUWriteMultipleResponse()
        write_response_pdu.from_bytes(response.pdu)

        if write_response_pdu.starting_address != starting_address:
            raise ValueError(
                f"invalid starting address in response, expect {starting_address} but received {write_response_pdu.starting_address}"
            )

        if write_response_pdu.quantity != len(values):
            raise ValueError(
                f"invalid quantity in response, expect {len(values)} but received {write_response_pdu.quantity}"
            )

        logger.info(
            f"Successfully write multiple registers from {starting_address} to {starting_address + len(values) - 1} with values: {values}"
        )

    async def read_variable(
        self,
        unit_id: int,
        address: int,
        num_registers: Literal[1, 2, 4],
        type: Literal["int", "float"],
        signed: bool = False,
        writable: bool = False,
        byte_order: Literal["big", "little"] = "big",
        word_order: Literal["big", "little"] = "big",
    ) -> int | float:
        """
        Reads a variable from the Modbus server.

        Args:
            unit_id (int): The unit ID.
            address (int): The address of the variable.
            num_registers (Literal[1, 2, 4]): The number of registers to read.
            type (Literal["int", "float"]): The type of the variable.
            signed (bool, optional): Whether the variable is signed. Defaults to False.
            writable (bool, optional): Whether the variable is writable. Defaults to False and read from holding registers.
            byte_order (Literal["big", "little"], optional): The byte order. Defaults to "big".
            word_order (Literal["big", "little"], optional): The word order. Defaults to "big".

        Returns:
            int | float: The value of the variable.

        Raises:
            ValueError: If there is a Modbus error.
        """
        if writable:
            registers = await self.read_holding_registers(
                unit_id, address, num_registers
            )
        else:
            registers = await self.read_input_registers(unit_id, address, num_registers)

        return deserialize(
            registers, type, signed, byte_order, word_order
        )

