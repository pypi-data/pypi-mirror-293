# ModbusPy

ModbusPy is a Python library for Modbus protocol. Implemented with asyncio and supports TCP, Serial.

## Installation

```bash
pip install modbuspy
```
## Usage

### TCP Server

```python
from modbuspy.Server.TCPServer import TCPServer

server = TCPServer(host="127.0.0.1", port=1502)

# Add a slave to the server
slave = server.add_slave(1)

# Add coils to the slave
coils = {i: bool(i % 2) for i in range(10)}  # Alternating True and False
slave.add_coils(coils)

# Add discrete inputs to the slave
discrete_inputs = {i: bool((i + 1) % 2) for i in range(10)}  # Alternating False and True
slave.add_discrete_inputs(discrete_inputs)

# Add holding registers to the slave
registers = {i: struct.pack("<h", i) for i in range(10)}  # 10 holding registers starting from 0
slave.add_holding_registers(registers)

# Add input registers to the slave
input_registers = {i: struct.pack("<h", i) for i in range(10)}  # 10 input registers starting from 0
slave.add_input_registers(input_registers)

# Add a variable to the slave
slave.add_variable(12345, 11, 2, signed=False, writable=True) # 12345 is the value, 11 is the starting address, 2 is the number of registers, writable determine if it is a holding register or input register

# Start the server
await server.start()
```

### TCP Client

```python
from modbuspy.Client.TCPClient import TCPClient

# Connect to the server
client = TCPClient(host="127.0.0.1", port=1502)
await client.connect()

# Read coils
coils = await client.read_coils(1, 0, 10)
print(coils)

# Write to coils
await client.write_coils(1, 0, [True, False, True, False, True, False, True, False, True, False])

# Read discrete inputs
inputs = await client.read_discrete_inputs(1, 0, 10)
print(inputs)

# Read holding registers
registers = await client.read_holding_registers(1, 0, 10)
print(registers)

# Write to holding registers
await client.write_holding_registers(1, 0, [struct.pack("<h", i) for i in range(10)])

# Read input registers
input_registers = await client.read_input_registers(1, 0, 10)
print(input_registers)

# Read a variable
variable = await client.read_variable(1, 11, 2)
print(variable)
```

### Serial Server and Client

They follow the same structure as the TCP server and client, but uses Serial as the transport layer.
