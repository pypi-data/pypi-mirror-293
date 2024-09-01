import io
import struct
from typing import Optional

from modbuspy import READ_COIL


class PDUErrorResponse:
    def __init__(
        self, function_code: Optional[int] = None, error_code: Optional[int] = None
    ) -> None:
        """
        Initializes a PDUErrorResponse instance.

        Args:
            function_code (Optional[int]): The function code.
            error_code (Optional[int]): The error code.
        """
        self._function_code: int | None = function_code
        self._error_code: int | None = error_code

    @property
    def function_code(self) -> int:
        if self._function_code is None:
            raise ValueError("function_code is not set")
        return self._function_code | 0x80

    @property
    def error_code(self) -> int:
        if self._error_code is None:
            raise ValueError("error_code is not set")
        return self._error_code

    @error_code.setter
    def error_code(self, value: int) -> None:
        self._error_code = value

    def to_bytes(self) -> bytes:
        """
        Converts the PDUErrorResponse instance to bytes.

        Returns:
            bytes: The byte representation of the PDUErrorResponse.
        """
        try:
            buffer = io.BytesIO()
            buffer.write(struct.pack("B", self.function_code))
            buffer.write(struct.pack("B", self.error_code))
            return buffer.getvalue()
        except Exception as e:
            raise ValueError(f"failed to convert PDUErrorResponse to bytes: {e}")

    def from_bytes(self, data: bytes) -> None:
        """
        Parses bytes to populate the PDUErrorResponse instance.

        Args:
            data (bytes): The byte data to parse.

        Raises:
            ValueError: If parsing fails.
        """
        try:
            buffer = io.BytesIO(data)
            self._function_code = struct.unpack("B", buffer.read(1))[0]
            self._error_code = struct.unpack("B", buffer.read(1))[0]
        except Exception as e:
            raise ValueError(f"failed to parse PDUErrorResponse: {e}")


class PDUReadResponse:
    def __init__(
        self, function_code: Optional[int] = None, data: Optional[bytes] = None
    ) -> None:
        """
        Initializes a PDUReadResponse instance.

        Args:
            function_code (Optional[int]): The function code.
            data (Optional[bytes]): The data bytes.
        """
        self._function_code: int | None = function_code
        self._data: bytes | None = data

    @property
    def function_code(self) -> int:
        if self._function_code is None:
            raise ValueError("function_code is not set")
        return self._function_code

    @property
    def data(self) -> bytes:
        if self._data is None:
            raise ValueError("data is not set")
        return self._data

    @data.setter
    def data(self, value: bytes) -> None:
        self._data = value

    def to_bytes(self) -> bytes:
        """
        Converts the PDUReadResponse instance to bytes.

        Returns:
            bytes: The byte representation of the PDUReadResponse.
        """
        try:
            buffer = io.BytesIO()
            buffer.write(struct.pack("B", self.function_code))
            buffer.write(struct.pack("B", len(self.data)))
            buffer.write(self.data)
            return buffer.getvalue()
        except Exception as e:
            raise ValueError(f"failed to convert PDUReadResponse to bytes: {e}")

    def from_bytes(self, data: bytes) -> None:
        """
        Parses bytes to populate the PDUReadResponse instance.

        Args:
            data (bytes): The byte data to parse.

        Raises:
            ValueError: If there is a mismatch in data length or parsing fails.
        """
        try:
            buffer = io.BytesIO(data)
            self._function_code = struct.unpack("B", buffer.read(1))[0]
            self.byte_count = struct.unpack("B", buffer.read(1))[0]
            self.data = buffer.read()
            if len(self.data) != self.byte_count:
                raise ValueError(
                    f"data length mismatch, expected {self.byte_count}, got {len(self.data)}"
                )
        except Exception as e:
            raise ValueError(f"failed to parse PDUReadResponse: {e}")


class PDUWriteSingleResponse:
    def __init__(
        self,
        function_code: Optional[int] = None,
        address: Optional[int] = None,
        value: Optional[bytes] = None,
    ) -> None:
        """
        Initializes a PDUWriteSingleResponse instance.

        Args:
            function_code (Optional[int]): The function code.
            address (Optional[int]): The output address.
            value (Optional[int]): The output value.
        """
        self._function_code: int | None = function_code
        self._address: int | None = address
        self._value: bytes | None = value

    @property
    def function_code(self) -> int:
        if self._function_code is None:
            raise ValueError("function_code is not set")
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
        """
        Converts the PDUWriteSingleResponse instance to bytes.

        Returns:
            bytes: The byte representation of the PDUWriteSingleResponse.
        """
        try:
            buffer = io.BytesIO()
            buffer.write(struct.pack("B", self.function_code))
            buffer.write(struct.pack(">H", self.address))
            buffer.write(self.value)
            return buffer.getvalue()
        except Exception as e:
            raise ValueError(f"failed to convert PDUWriteSingleResponse to bytes: {e}")

    def from_bytes(self, data: bytes) -> None:
        """
        Parses bytes to populate the PDUWriteSingleResponse instance.

        Args:
            data (bytes): The byte data to parse.

        Raises:
            ValueError: If parsing fails.
        """
        try:
            buffer = io.BytesIO(data)
            self._function_code = struct.unpack("B", buffer.read(1))[0]
            self.address = struct.unpack(">H", buffer.read(2))[0]
            self.value = buffer.read()
        except Exception as e:
            raise ValueError(f"failed to parse PDUWriteSingleResponse: {e}")


class PDUWriteMultipleResponse:
    def __init__(
        self,
        function_code: Optional[int] = None,
        starting_address: Optional[int] = None,
        quantity: Optional[int] = None,
    ) -> None:
        """
        Initializes a PDUWriteMultipleResponse instance.

        Args:
            function_code (Optional[int]): The function code.
            starting_address (Optional[int]): The starting address.
            quantity (Optional[int]): The quantity.
        """
        self._function_code: int | None = function_code
        self._starting_address: int | None = starting_address
        self._quantity: int | None = quantity

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

    @property
    def quantity(self) -> int:
        if self._quantity is None:
            raise ValueError("quantity is not set")
        return self._quantity

    @starting_address.setter
    def starting_address(self, value: int) -> None:
        self._starting_address = value

    @quantity.setter
    def quantity(self, value: int) -> None:
        self._quantity = value

    def to_bytes(self) -> bytes:
        """
        Converts the PDUWriteMultipleResponse instance to bytes.

        Returns:
            bytes: The byte representation of the PDUWriteMultipleResponse.
        """
        try:
            buffer = io.BytesIO()
            buffer.write(struct.pack("B", self.function_code))
            buffer.write(struct.pack(">H", self.starting_address))
            buffer.write(struct.pack(">H", self.quantity))
            return buffer.getvalue()
        except Exception as e:
            raise ValueError(
                f"failed to convert PDUWriteMultipleResponse to bytes: {e}"
            )

    def from_bytes(self, data: bytes) -> None:
        """
        Parses bytes to populate the PDUWriteMultipleResponse instance.

        Args:
            data (bytes): The byte data to parse.

        Raises:
            ValueError: If parsing fails.
        """
        try:
            buffer = io.BytesIO(data)
            self._function_code = struct.unpack("B", buffer.read(1))[0]
            self.starting_address = struct.unpack(">H", buffer.read(2))[0]
            self.quantity = struct.unpack(">H", buffer.read(2))[0]
        except Exception as e:
            raise ValueError(f"failed to parse PDUWriteMultipleResponse: {e}")
