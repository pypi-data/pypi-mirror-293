from __future__ import annotations
import struct
from modbuspy import logger
from typing import Callable, Literal, Optional


class Coil:
    def __init__(
        self,
        slave: Slave,
        address: int,
        value: bool,
        read_function: Optional[Callable[[], bool]] = None,
        write_function: Optional[Callable[[bool], None]] = None,
    ):
        """Initializes a Coil instance.

        Args:
            slave (Slave): The slave to which the coil belongs.
            address (int): The address of the coil.
            value (bool): The value of the coil.
            read_function (Optional[Callable[[], bool]], optional): The read function of the coil. Defaults to None.
            write_function (Optional[Callable[[bool], None]], optional): The write function of the coil. Defaults to None.
        """
        self._slave = slave
        self._address = address
        if isinstance(value, bytes):
            self._value = value == b"\xFF\x00"
        else:
            self._value = value
        self._read_function = read_function
        self._write_function = write_function

    @property
    def value(self) -> bool:
        """Gets the value of the coil.

        Returns:
            bool: The value of the coil.
        """
        return self._value

    @value.setter
    def value(self, value: bool) -> None:
        """Sets the value of the coil.

        Args:
            value (bool): The new value of the coil.
        """
        self._value = value

class DiscreteInput:
    def __init__(
        self,
        slave: Slave,
        address: int,
        value: bool | bytes,
        read_function: Optional[Callable[[], bool]] = None,
        write_function: Optional[Callable[[bool], None]] = None,
    ):
        """Initializes a DiscreteInput instance.

        Args:
            slave (Slave): The slave to which the discrete input belongs.
            address (int): The address of the discrete input.
            value (bool | bytes): The value of the discrete input.
            read_function (Optional[Callable[[], bool]], optional): The read function of the discrete input. Defaults to None.
            write_function (Optional[Callable[[bool], None]], optional): The write function of the discrete input. Defaults to None.
        """
        self._slave = slave
        self._address = address
        if isinstance(value, bytes):
            self._value = value == b"\xFF\x00"
        else:
            self._value = value
        self._read_function = read_function
        self._write_function = write_function

    @property
    def value(self) -> bytes:
        """Gets the value of the discrete input.

        Returns:
            bytes: The value of the discrete input as bytes.
        """
        return b"\xFF\x00" if self._value else b"\x00\x00"

    @value.setter
    def value(self, value: bool | bytes) -> None:
        """Sets the value of the discrete input.

        Args:
            value (bool | bytes): The new value of the discrete input.

        Raises:
            TypeError: If the value is not a bool or bytes.
        """
        if isinstance(value, bool):
            self._value = value
        elif isinstance(value, bytes):
            self._value = value == b"\xFF\x00"
        else:
            raise TypeError("value must be a bool or bytes")


class HoldingRegister:
    def __init__(
        self,
        slave: Slave,
        address: int,
        value: bytes,
        read_function: Optional[Callable[[], bytes]] = None,
        write_function: Optional[Callable[[bytes], None]] = None,
    ):
        """Initializes a HoldingRegister instance.

        Args:
            slave (Slave): The slave to which the holding register belongs.
            address (int): The address of the holding register.
            value (bytes): The value of the holding register.
            read_function (Optional[Callable[[], bytes]], optional): The read function of the holding register. Defaults to None.
            write_function (Optional[Callable[[bytes], None]], optional): The write function of the holding register. Defaults to None.
        """
        self._slave = slave
        self._address = address
        self._value = value
        self._read_function = read_function
        self._write_function = write_function

    @property
    def value(self) -> bytes:
        """Gets the value of the holding register.

        Returns:
            bytes: The value of the holding register as bytes.
        """
        return self._value
    
    @value.setter
    def value(self, value: bytes) -> None:
        """Sets the value of the holding register.

        Args:
            value (bytes): The new value of the holding register.
        """
        self._value = value


class InputRegister:
    def __init__(
        self,
        slave: Slave,
        address: int,
        value: bytes,
        read_function: Optional[Callable[[], bytes]] = None,
        write_function: Optional[Callable[[bytes], None]] = None,
    ):
        """Initializes an InputRegister instance.

        Args:
            slave (Slave): The slave to which the input register belongs.
            address (int): The address of the input register.
            value (bytes): The value of the input register.
            read_function (Optional[Callable[[], bytes]], optional): The read function of the input register. Defaults to None.
            write_function (Optional[Callable[[bytes], None]], optional): The write function of the input register. Defaults to None.
        """
        self._slave = slave
        self._address = address
        self._value = value
        self._read_function = read_function
        self._write_function = write_function

    @property
    def value(self) -> bytes:
        """Gets the value of the input register.

        Returns:
            bytes: The value of the input register as bytes.
        """
        return self._value


class Slave:
    def __init__(
        self,
        byte_order: Literal["big", "little"] = "big",
        word_order: Literal["big", "little"] = "big",
    ):
        """Initializes the Slave with empty dictionaries for Modbus data types.

        Args:
            byte_order (Literal["big", "little"], optional): Byte order, either 'big' or 'little'. Defaults to 'big'.
            word_order (Literal["big", "little"], optional): Word order, either 'big' or 'little'. Defaults to 'big'.

        Attributes:
            coils (dict): Dictionary to store coil values.
            discrete_inputs (dict): Dictionary to store discrete input values.
            holding_registers (dict): Dictionary to store holding register values.
            input_registers (dict): Dictionary to store input register values.
        """
        self._byte_order: Literal["big", "little"] = byte_order
        self._word_order: Literal["big", "little"] = word_order
        self.coils: dict[int, Coil] = {}
        self.discrete_inputs: dict[int, DiscreteInput] = {}
        self.holding_registers: dict[int, HoldingRegister] = {}
        self.input_registers: dict[int, InputRegister] = {}

    def add_coil(
        self,
        address: int,
        value: bool,
        read_function: Optional[Callable[[], bool]] = None,
        write_function: Optional[Callable[[bool], None]] = None,
    ) -> None:
        """Adds a single coil to the slave.

        Args:
            address (int): The address of the coil.
            value (bool): The value of the coil.
            read_function (Optional[Callable[[], bool]], optional): The read function of the coil. Defaults to None.
            write_function (Optional[Callable[[bool], None]], optional): The write function of the coil. Defaults to None.
        """
        if address in self.coils:
            logger.warning(f"Coil at address {address} already exists. Overwriting.")
        self.coils[address] = Coil(self, address, value, read_function, write_function)

    def add_coils(
        self,
        coils: dict[int, bool],
        read_function: Optional[Callable[[], bool]] = None,
        write_function: Optional[Callable[[bool], None]] = None,
    ) -> None:
        """Adds multiple coils to the slave.

        Args:
            coils (dict[int, bool]): A dictionary of coil addresses and their values.
            read_function (Optional[Callable[[], bool]], optional): The read function of the coil. Defaults to None.
            write_function (Optional[Callable[[bool], None]], optional): The write function of the coil. Defaults to None.
        """
        for address, value in coils.items():
            self.add_coil(address, value, read_function, write_function)

    def add_discrete_input(
        self,
        address: int,
        value: bool,
        read_function: Optional[Callable[[], bool]] = None,
        write_function: Optional[Callable[[bool], None]] = None,
    ) -> None:
        """Adds a single discrete input to the slave.

        Args:
            address (int): The address of the discrete input.
            value (bool): The value of the discrete input.
            read_function (Optional[Callable[[], bool]], optional): The read function of the discrete input. Defaults to None.
            write_function (Optional[Callable[[bool], None]], optional): The write function of the discrete input. Defaults to None.
        """
        if address in self.discrete_inputs:
            logger.warning(
                f"Discrete input at address {address} already exists. Overwriting."
            )
        self.discrete_inputs[address] = DiscreteInput(
            self, address, value, read_function, write_function
        )

    def add_discrete_inputs(
        self,
        discrete_inputs: dict[int, bool],
        read_function: Optional[Callable[[], bool]] = None,
        write_function: Optional[Callable[[bool], None]] = None,
    ) -> None:
        """Adds multiple discrete inputs to the slave.

        Args:
            discrete_inputs (dict[int, bool]): A dictionary of discrete input addresses and their values.
            read_function (Optional[Callable[[], bool]], optional): The read function of the discrete input. Defaults to None.
            write_function (Optional[Callable[[bool], None]], optional): The write function of the discrete input. Defaults to None.
        """
        for address, value in discrete_inputs.items():
            self.add_discrete_input(address, value, read_function, write_function)

    def add_holding_register(
        self,
        address: int,
        value: bytes,
        read_function: Optional[Callable[[], bytes]] = None,
        write_function: Optional[Callable[[bytes], None]] = None,
    ) -> None:
        """Adds a single holding register to the slave with automatic conversion to binary.

        Args:
            address (int): The starting address of the holding register.
            value (bytes): The value of the holding register.
            read_function (Optional[Callable[[], bytes]], optional): The read function of the holding register. Defaults to None.
            write_function (Optional[Callable[[bytes], None]], optional): The write function of the holding register. Defaults to None.
        """
        if address in self.holding_registers:
            logger.warning(
                f"Holding register at address {address} already exists. Overwriting."
            )
        self.holding_registers[address] = HoldingRegister(
            self, address, value, read_function, write_function
        )

    def add_holding_registers(
        self,
        registers: dict[int, bytes],
        read_function: Optional[Callable[[], bytes]] = None,
        write_function: Optional[Callable[[bytes], None]] = None,
    ) -> None:
        """Adds multiple holding registers to the slave with automatic conversion to binary.

        Args:
            registers (dict[int, bytes]): A dictionary of holding register addresses and their values.
            read_function (Optional[Callable[[], bytes]], optional): The read function of the holding register. Defaults to None.
            write_function (Optional[Callable[[bytes], None]], optional): The write function of the holding register. Defaults to None.
        """
        for address, value in registers.items():
            self.holding_registers[address] = HoldingRegister(
                self, address, value, read_function, write_function
            )

    def add_input_register(
        self,
        address: int,
        value: bytes,
        read_function: Optional[Callable[[], bytes]] = None,
        write_function: Optional[Callable[[bytes], None]] = None,
    ) -> None:
        """Adds a single input register to the slave with automatic conversion to binary.

        Args:
            address (int): The starting address of the input register.
            value (bytes): The value of the input register.
            read_function (Optional[Callable[[], bytes]], optional): The read function of the input register. Defaults to None.
            write_function (Optional[Callable[[bytes], None]], optional): The write function of the input register. Defaults to None.
        """
        if address in self.input_registers:
            logger.warning(
                f"Input register at address {address} already exists. Overwriting."
            )
        self.input_registers[address] = InputRegister(
            self, address, value, read_function, write_function
        )

    def add_input_registers(
        self,
        registers: dict[int, bytes],
        read_function: Optional[Callable[[], bytes]] = None,
        write_function: Optional[Callable[[bytes], None]] = None,
    ) -> None:
        """Adds multiple input registers to the slave with automatic conversion to binary.

        Args:
            registers (dict[int, bytes]): A dictionary of input register addresses and their values.
            read_function (Optional[Callable[[], bytes]], optional): The read function of the input register. Defaults to None.
            write_function (Optional[Callable[[bytes], None]], optional): The write function of the input register. Defaults to None.
        """
        for address, value in registers.items():
            self.input_registers[address] = InputRegister(
                self, address, value, read_function, write_function
            )
