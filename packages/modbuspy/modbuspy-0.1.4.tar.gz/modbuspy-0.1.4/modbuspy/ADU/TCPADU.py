import io
import struct
from typing import Literal, Optional
from modbuspy.ADU import MODBUS_EXCEPTION_MESSAGES


class TCPADU:
    def __init__(
        self,
        transaction_id: Optional[int] = None,
        unit_id: Optional[int] = None,
        pdu: Optional[bytes] = None,
    ) -> None:
        """
        Initializes a TCPADU instance.

        Args:
            transaction_id (Optional[int]): The transaction ID.
            unit_id (Optional[int]): The unit ID.
            pdu (Optional[bytes]): The Protocol Data Unit.
        """
        self._transaction_id = transaction_id
        self._unit_id = unit_id
        self._pdu = pdu

    @property
    def transaction_id(self) -> int:
        if self._transaction_id is None:
            raise ValueError("transaction_id is not set")
        return self._transaction_id

    @transaction_id.setter
    def transaction_id(self, value: int) -> None:
        self._transaction_id = value

    @property
    def protocol_id(self) -> int:
        return 0

    @property
    def length(self) -> int:
        return 1 + len(self.pdu) if self.pdu else 1

    @property
    def unit_id(self) -> int:
        if self._unit_id is None:
            raise ValueError("unit_id is not set")
        return self._unit_id

    @unit_id.setter
    def unit_id(self, value: int) -> None:
        self._unit_id = value

    @property
    def pdu(self) -> bytes:
        if self._pdu is None:
            raise ValueError("pdu is not set")
        return self._pdu

    @pdu.setter
    def pdu(self, value: bytes) -> None:
        self._pdu = value

    def is_error(self) -> tuple[bool, str]:
        if self.pdu[0] >= 0x80:
            exception_code = self.pdu[1]
            err = MODBUS_EXCEPTION_MESSAGES.get(exception_code, "Unknown exception code")
            return True, err
        return False, ""

    def to_bytes(self) -> bytes:
        """
        Converts the TCPADU instance to bytes.

        Returns:
            bytes: The byte representation of the TCPADU instance.
        """
        try:
            buffer = io.BytesIO()
            buffer.write(struct.pack(">H", self.transaction_id))
            buffer.write(struct.pack(">H", self.protocol_id))
            buffer.write(struct.pack(">H", self.length))
            buffer.write(struct.pack("B", self.unit_id))
            buffer.write(self.pdu)
            return buffer.getvalue()
        except Exception as e:
            raise ValueError(f"failed to convert TCPADU to bytes: {e}")

    def from_bytes(self, data: bytes) -> None:
        """
        Parses bytes to populate the TCPADU instance.

        Args:
            data (bytes): The byte data to parse.

        Raises:
            ValueError: If the PDU length is invalid or parsing fails.
        """
        buffer = io.BytesIO(data)
        try:
            self.transaction_id = struct.unpack(">H", buffer.read(2))[0]
            protocol_id = struct.unpack(">H", buffer.read(2))[0]
            if protocol_id != 0:
                raise ValueError("invalid protocol ID")
            length = struct.unpack(">H", buffer.read(2))[0]
            self.unit_id = struct.unpack("B", buffer.read(1))[0]
            self.pdu = buffer.read()
            if self.length != length:
                raise ValueError("invalid PDU length")
        except Exception as e:
            raise ValueError(f"failed to parse TCPADU: {e}")
