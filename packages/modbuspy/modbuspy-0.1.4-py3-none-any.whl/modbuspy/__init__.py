import logging
import struct
from typing import Literal
import colorlog


# Configure logging
formatter = colorlog.ColoredFormatter(
    "%(log_color)s%(levelname)s:%(name)s:%(message)s",
    log_colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "red,bg_white",
    },
)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

file_handler = logging.FileHandler("modbuspy.log")
file_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)

logging.basicConfig(level=logging.INFO, handlers=[stream_handler, file_handler])
logger = logging.getLogger(__name__)

# Constants
READ_COIL = 0x01
READ_DISCRETE_INPUT = 0x02
READ_HOLDING_REGISTER = 0x03
READ_INPUT_REGISTER = 0x04
WRITE_SINGLE_COIL = 0x05
WRITE_SINGLE_REGISTER = 0x06
WRITE_MULTIPLE_COILS = 0x0F
WRITE_MULTIPLE_REGISTERS = 0x10


def _struct_int_format(
    num_registers: Literal[1, 2, 4],
    byte_order: Literal["big", "little"] = "big",
    signed: bool = False,
) -> str:
    _byte_order = ">" if byte_order == "big" else "<"
    if num_registers == 1:
        if signed:
            return f"{_byte_order}h"
        else:
            return f"{_byte_order}H"
    elif num_registers == 2:
        if signed:
            return f"{_byte_order}i"
        else:
            return f"{_byte_order}I"
    elif num_registers == 4:
        if signed:
            return f"{_byte_order}q"
        else:
            return f"{_byte_order}Q"


def _struct_float_format(
    num_registers: Literal[1, 2, 4],
    byte_order: Literal["big", "little"] = "big",
) -> str:
    _byte_order = ">" if byte_order == "big" else "<"
    if num_registers == 1:
        return f"{_byte_order}f"
    if num_registers == 2:
        return f"{_byte_order}f"
    elif num_registers == 4:
        return f"{_byte_order}d"


def serialize(
    value: int | float,
    num_registers: Literal[1, 2, 4],
    signed: bool = False,
    byte_order: Literal["big", "little"] = "big",
    word_order: Literal["big", "little"] = "big",
) -> list[bytes]:
    serialized_values: list[bytes] = []
    if isinstance(value, int):
        fmt = _struct_int_format(num_registers, byte_order, signed)
        value_bytes = struct.pack(fmt, value)
        for i in range(0, len(value_bytes), 2):
            serialized_values.append(value_bytes[i : i + 2])
        if word_order == "big":
            logger.debug(f"Serialized int: {serialized_values}")
            return serialized_values
        else:
            logger.debug(f"Serialized int: {serialized_values[::-1]}")
            return serialized_values[::-1]
    elif isinstance(value, float):
        fmt = _struct_float_format(num_registers, byte_order)
        value_bytes = struct.pack(fmt, value)
        for i in range(0, len(value_bytes), 2):
            serialized_values.append(value_bytes[i : i + 2])
        if word_order == "big":
            logger.debug(f"Serialized float: {serialized_values}")
            return serialized_values
        else:
            logger.debug(f"Serialized float: {serialized_values[::-1]}")
            return serialized_values[::-1]

def deserialize(
    values: list[bytes],
    type: Literal["int", "float"],
    signed: bool = False,
    byte_order: Literal["big", "little"] = "big",
    word_order: Literal["big", "little"] = "big",
) -> int | float:
    if word_order == "little":
        values = values[::-1]
    if type == "int":
        num_registers = len(values)
        if num_registers not in [1, 2, 4]:
            raise ValueError(f"Invalid number of registers: {num_registers}")
        fmt = _struct_int_format(num_registers, byte_order, signed) # type: ignore
        value = struct.unpack(fmt, b''.join(values))[0]
        logger.debug(f"Deserialized int: {value}")
        return value
    elif type == "float":
        num_registers = len(values)
        if num_registers not in [2, 4]:
            raise ValueError(f"Invalid number of registers: {num_registers}")
        fmt = _struct_float_format(num_registers, byte_order) # type: ignore
        value = struct.unpack(fmt, b''.join(values))[0]
        logger.debug(f"Deserialized float: {value}")
        return value

