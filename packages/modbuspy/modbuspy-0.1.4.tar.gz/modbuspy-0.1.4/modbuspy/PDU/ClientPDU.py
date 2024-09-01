import io
import struct
from typing import Optional

from modbuspy import (
    READ_COIL,
    READ_DISCRETE_INPUT,
    READ_HOLDING_REGISTER,
    READ_INPUT_REGISTER,
    WRITE_MULTIPLE_COILS,
    WRITE_MULTIPLE_REGISTERS,
    WRITE_SINGLE_COIL,
    WRITE_SINGLE_REGISTER,
)


class PDURead:
    def __init__(
        self,
        function_code: Optional[int] = None,
        starting_address: Optional[int] = None,
        quantity: Optional[int] = None,
    ) -> None:
        """Initializes a PDURead instance.

        Args:
            function_code (Optional[int]): The Modbus function code.
            starting_address (Optional[int]): The starting address for the read operation.
            quantity (Optional[int]): The number of items to read.
        """
        self._function_code = function_code
        self._starting_address = starting_address
        self._quantity = quantity

    @property
    def function_code(self) -> int:
        if self._function_code is None:
            raise ValueError("function_code is not set")
        return self._function_code

    @property
    def starting_address(self) -> int:
        if self._starting_address is None:
            raise ValueError("starting_address is not set")
        return self._starting_address

    @starting_address.setter
    def starting_address(self, value: int) -> None:
        self._starting_address = value

    @property
    def quantity(self) -> int:
        if self._quantity is None:
            raise ValueError("quantity is not set")
        return self._quantity

    @quantity.setter
    def quantity(self, value: int) -> None:
        self._quantity = value

    def to_bytes(self) -> bytes:
        """Converts the PDURead instance to bytes.

        Returns:
            bytes: The byte representation of the PDURead instance.
        """
        try:
            buffer = io.BytesIO()
            buffer.write(struct.pack("B", self.function_code))
            buffer.write(struct.pack(">H", self.starting_address))
            buffer.write(struct.pack(">H", self.quantity))
            return buffer.getvalue()
        except Exception as e:
            raise ValueError(f"failed to convert PDURead to bytes: {e}")

    def from_bytes(self, data: bytes) -> None:
        """Parses bytes to populate the PDURead instance.

        Args:
            data (bytes): The byte data to parse.
        """
        try:
            buffer = io.BytesIO(data)
            self._function_code = struct.unpack("B", buffer.read(1))[0]
            self.starting_address = struct.unpack(">H", buffer.read(2))[0]
            self.quantity = struct.unpack(">H", buffer.read(2))[0]
        except Exception as e:
            raise ValueError(f"failed to parse PDURead: {e}")


class PDUReadCoils(PDURead):
    def __init__(
        self, starting_address: Optional[int] = None, quantity: Optional[int] = None
    ) -> None:
        """Initializes a PDUReadCoils instance.

        Args:
            starting_address (Optional[int]): The starting address for the read operation.
            quantity (Optional[int]): The number of coils to read.
        """
        super().__init__(READ_COIL, starting_address, quantity)


class PDUReadDiscreteInputs(PDURead):
    def __init__(
        self, starting_address: Optional[int] = None, quantity: Optional[int] = None
    ) -> None:
        """Initializes a PDUReadDiscreteInputs instance.

        Args:
            starting_address (Optional[int]): The starting address for the read operation.
            quantity (Optional[int]): The number of discrete inputs to read.
        """
        super().__init__(READ_DISCRETE_INPUT, starting_address, quantity)


class PDUReadHoldingRegisters(PDURead):
    def __init__(
        self, starting_address: Optional[int] = None, quantity: Optional[int] = None
    ) -> None:
        """Initializes a PDUReadHoldingRegisters instance.

        Args:
            starting_address (Optional[int]): The starting address for the read operation.
            quantity (Optional[int]): The number of holding registers to read.
        """
        super().__init__(READ_HOLDING_REGISTER, starting_address, quantity)


class PDUReadInputRegisters(PDURead):
    def __init__(
        self, starting_address: Optional[int] = None, quantity: Optional[int] = None
    ) -> None:
        """Initializes a PDUReadInputRegisters instance.

        Args:
            starting_address (Optional[int]): The starting address for the read operation.
            quantity (Optional[int]): The number of input registers to read.
        """
        super().__init__(READ_INPUT_REGISTER, starting_address, quantity)


class PDUWriteSingleCoil:
    def __init__(
        self, address: Optional[int] = None, value: Optional[bool] = None
    ) -> None:
        """Initializes a PDUWriteSingleCoil instance.

        Args:
            address (Optional[int]): The address of the coil to write.
            value (Optional[bool]): The value to write to the coil.
        """
        self._function_code: int = WRITE_SINGLE_COIL
        self._address: int | None = address
        self._value: bool | None = value

    @property
    def function_code(self) -> int:
        return self._function_code

    @property
    def address(self) -> int:
        if self._address is None:
            raise ValueError("address is not set")
        return self._address

    @address.setter
    def address(self, value: int) -> None:
        self._address = value

    @property
    def value(self) -> bool:
        if self._value is None:
            raise ValueError("value is not set")
        return self._value

    @value.setter
    def value(self, value: bool) -> None:
        self._value = value

    def to_bytes(self) -> bytes:
        """Converts the PDUWriteSingleCoil instance to bytes.

        Returns:
            bytes: The byte representation of the PDUWriteSingleCoil instance.
        """
        try:
            buffer = io.BytesIO()
            buffer.write(struct.pack("B", self.function_code))
            buffer.write(struct.pack(">H", self.address))
            if self.value:
                buffer.write(b"\xFF\x00")
            else:
                buffer.write(b"\x00\x00")
            return buffer.getvalue()
        except Exception as e:
            raise ValueError(f"failed to convert PDUWriteSingleCoil to bytes: {e}")

    def from_bytes(self, data: bytes) -> None:
        """Parses bytes to populate the PDUWriteSingleCoil instance.

        Args:
            data (bytes): The byte data to parse.

        Raises:
            ValueError: If the function code is not WRITE_SINGLE_COIL.
        """
        try:
            buffer = io.BytesIO(data)
            function_code = struct.unpack("B", buffer.read(1))[0]
            if function_code != WRITE_SINGLE_COIL:
                raise ValueError(
                    f"function_code is expected to be {WRITE_SINGLE_COIL}, but got {function_code}"
                )
            self._function_code = function_code
            self.address = struct.unpack(">H", buffer.read(2))[0]
            value = buffer.read(2)
            if value == b"\xFF\x00":
                self._value = True
            elif value == b"\x00\x00":
                self._value = False
            else:
                raise ValueError(
                    f"value is expected to be {b'\xFF\x00'} or {b'\x00\x00'}, but got {value}"
                )
        except Exception as e:
            raise ValueError(f"failed to parse PDUWriteSingleCoil: {e}")


class PDUWriteMultipleCoils:
    def __init__(
        self,
        starting_address: Optional[int] = None,
        values: Optional[list[bool]] = None,
    ) -> None:
        """Initializes a PDUWriteMultipleCoils instance.

        Args:
            starting_address (Optional[int]): The starting address for the write operation.
            values (Optional[list[bool]]): The values to write to the coils.
        """
        self._function_code: int = WRITE_MULTIPLE_COILS
        self._starting_address = starting_address
        self._values = values

    @property
    def function_code(self) -> int:
        return self._function_code

    @property
    def values(self) -> list[bool]:
        if self._values is None:
            raise ValueError("values is not set")
        return self._values

    @values.setter
    def values(self, values: list[bool]) -> None:
        self._values = values

    @property
    def starting_address(self) -> int:
        if self._starting_address is None:
            raise ValueError("starting_address is not set")
        return self._starting_address

    @starting_address.setter
    def starting_address(self, value: int) -> None:
        self._starting_address = value

    def to_bytes(self) -> bytes:
        """Converts the PDUWriteMultipleCoils instance to bytes.

        Returns:
            bytes: The byte representation of the PDUWriteMultipleCoils instance.
        """

        def serialize_coils(values: list[bool]) -> bytes:
            byte_count = (len(values) + 7) // 8
            coil_data = bytearray(byte_count)

            for i, value in enumerate(values):
                if value:
                    coil_data[i // 8] |= 1 << (i % 8)

            return bytes(coil_data)

        try:
            buffer = io.BytesIO()
            buffer.write(struct.pack("B", self.function_code))
            buffer.write(struct.pack(">H", self.starting_address))
            buffer.write(struct.pack(">H", len(self.values)))
            serialized_values = serialize_coils(self.values)
            buffer.write(struct.pack("B", len(serialized_values)))
            buffer.write(serialized_values)
            return buffer.getvalue()
        except Exception as e:
            raise ValueError(f"failed to convert PDUWriteMultipleCoils to bytes: {e}")

    def from_bytes(self, data: bytes) -> None:
        """Parses bytes to populate the PDUWriteMultipleCoils instance.

        Args:
            data (bytes): The byte data to parse.

        Raises:
            ValueError: If the data length is insufficient.
        """

        def deserialize_coils(data: bytes, quantity: int) -> list[bool]:
            values = []
            for i in range(quantity):
                byte_index = i // 8
                bit_index = i % 8
                bit_value = (data[byte_index] >> bit_index) & 1
                values.append(bit_value == 1)
            return values

        try:
            buffer = io.BytesIO(data)
            self._function_code = struct.unpack("B", buffer.read(1))[0]
            self.starting_address = struct.unpack(">H", buffer.read(2))[0]
            quantity = struct.unpack(">H", buffer.read(2))[0]
            byte_count = struct.unpack("B", buffer.read(1))[0]
            values = deserialize_coils(buffer.read(byte_count), quantity)
            self.values = values
        except Exception as e:
            raise ValueError(f"failed to parse PDUWriteMultipleCoils: {e}")


class PDUWriteSingleRegister:
    def __init__(
        self, address: Optional[int] = None, value: Optional[bytes] = None
    ) -> None:
        """Initializes a PDUWriteSingleRegister instance.

        Args:
            address (Optional[int]): The address of the register to write.
            value (Optional[bytes]): The value to write to the register.
        """
        self._function_code: int = WRITE_SINGLE_REGISTER
        self._address: int | None = address
        self._value: bytes | None = value

    @property
    def function_code(self) -> int:
        return self._function_code

    @property
    def address(self) -> int:
        if self._address is None:
            raise ValueError("address is not set")
        return self._address

    @address.setter
    def address(self, value: int) -> None:
        self._address = value

    @property
    def value(self) -> bytes:
        if self._value is None:
            raise ValueError("value is not set")
        return self._value

    @value.setter
    def value(self, value: bytes) -> None:
        self._value = value

    def to_bytes(self) -> bytes:
        """Converts the PDUWriteSingleRegister instance to bytes.

        Returns:
            bytes: The byte representation of the PDUWriteSingleRegister instance.
        """
        try:
            buffer = io.BytesIO()
            buffer.write(struct.pack("B", self.function_code))
            buffer.write(struct.pack(">H", self.address))
            buffer.write(self.value)
            return buffer.getvalue()
        except Exception as e:
            raise ValueError(f"failed to convert PDUWriteSingleRegister to bytes: {e}")

    def from_bytes(self, data: bytes) -> None:
        """Parses bytes to populate the PDUWriteSingleRegister instance.

        Args:
            data (bytes): The byte data to parse.

        Raises:
            ValueError: If the function code is not WRITE_SINGLE_REGISTER.
        """
        try:
            buffer = io.BytesIO(data)
            function_code = struct.unpack("B", buffer.read(1))[0]
            if function_code != WRITE_SINGLE_REGISTER:
                raise ValueError(
                    f"function_code is expected to be {WRITE_SINGLE_REGISTER}, but got {function_code}"
                )
            self._function_code = function_code
            self.address = struct.unpack(">H", buffer.read(2))[0]
            self.value = buffer.read()
        except Exception as e:
            raise ValueError(f"failed to parse PDUWriteSingleRegister: {e}")


class PDUWriteMultipleRegisters:
    def __init__(
        self,
        starting_address: Optional[int] = None,
        values: Optional[list[bytes]] = None,
    ) -> None:
        """Initializes a PDUWriteMultipleRegisters instance.

        Args:
            starting_address (Optional[int]): The starting address for the write operation.
            values (Optional[list[bytes]]): The values to write to the registers.
        """
        self._function_code: int = WRITE_MULTIPLE_REGISTERS
        self._starting_address: int | None = starting_address
        self._values: list[bytes] | None = values

    @property
    def function_code(self) -> int:
        return self._function_code

    @property
    def starting_address(self) -> int:
        if self._starting_address is None:
            raise ValueError("starting_address is not set")
        return self._starting_address

    @starting_address.setter
    def starting_address(self, value: int) -> None:
        self._starting_address = value

    @property
    def values(self) -> list[bytes]:
        if self._values is None:
            raise ValueError("values is not set")
        return self._values

    @values.setter
    def values(self, values: list[bytes]) -> None:
        self._values = values

    def to_bytes(self) -> bytes:
        """Converts the PDUWriteMultipleRegisters instance to bytes.

        Returns:
            bytes: The byte representation of the PDUWriteMultipleRegisters instance.
        """
        try:
            buffer = io.BytesIO()
            buffer.write(struct.pack("B", self.function_code))
            buffer.write(struct.pack(">H", self.starting_address))
            buffer.write(struct.pack(">H", len(self.values)))  # quantity_of_outputs
            values = b"".join(self.values)  # concat values
            buffer.write(struct.pack("B", len(values)))  # byte_count
            buffer.write(values)
            return buffer.getvalue()
        except Exception as e:
            raise ValueError(
                f"failed to convert PDUWriteMultipleRegisters to bytes: {e}"
            )

    def from_bytes(self, data: bytes) -> None:
        """Parses bytes to populate the PDUWriteMultipleRegisters instance.

        Args:
            data (bytes): The byte data to parse.

        Raises:
            ValueError: If the function code is not WRITE_MULTIPLE_REGISTERS or data length is insufficient.
        """
        try:
            buffer = io.BytesIO(data)
            function_code = struct.unpack("B", buffer.read(1))[0]
            if function_code != WRITE_MULTIPLE_REGISTERS:
                raise ValueError(
                    f"function_code is expected to be {WRITE_MULTIPLE_REGISTERS}, but got {function_code}"
                )
            self._function_code = function_code
            self.starting_address = struct.unpack(">H", buffer.read(2))[0]
            quantity_of_outputs = struct.unpack(">H", buffer.read(2))[0]
            byte_count = struct.unpack("B", buffer.read(1))[0]
            if byte_count != quantity_of_outputs * 2:
                raise ValueError(
                    f"Expected {quantity_of_outputs * 2} bytes, but got {byte_count} bytes"
                )
            values = []
            for _ in range(quantity_of_outputs):
                values.append(buffer.read(2))
            self.values = values
        except Exception as e:
            raise ValueError(f"failed to parse PDUWriteMultipleRegisters: {e}")
