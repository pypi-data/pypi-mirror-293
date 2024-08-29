MODBUS_EXCEPTION_MESSAGES = {
    0x01: "Illegal Function",                # Function code received in the query is not recognized or allowed by the server.
    0x02: "Illegal Data Address",            # Data address of some or all the required entities are not allowed or do not exist in the server.
    0x03: "Illegal Data Value",              # Value is not accepted by the server.
    0x04: "Server Device Failure",           # Unrecoverable error occurred while the server was attempting to perform the requested action.
    0x05: "Acknowledge",                     # Specialized use in conjunction with programming commands.
    0x06: "Server Device Busy",              # Server is engaged in processing a long-duration command.
    0x08: "Memory Parity Error",             # Specialized use in conjunction with function codes 20 and 21, indicating a parity error in memory.
    0x0A: "Gateway Path Unavailable",        # Specialized use in conjunction with gateways, indicating that the gateway is misconfigured or overloaded.
    0x0B: "Gateway Target Device Failed to Respond", # Specialized use in conjunction with gateways, indicating no response was received from the target device.
}
