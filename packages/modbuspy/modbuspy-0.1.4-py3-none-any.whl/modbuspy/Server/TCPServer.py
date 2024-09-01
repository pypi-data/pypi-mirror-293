import asyncio
import ssl
from typing import Optional

from modbuspy.ADU.TCPADU import TCPADU
from modbuspy.PDU.ServerPDU import (
    PDUErrorResponse,
    PDUReadResponse,
    PDUWriteMultipleResponse,
    PDUWriteSingleResponse,
)
from modbuspy.Server import Server


class TCPServer(Server):
    def __init__(
        self,
        host: str,
        port: int,
        use_tls: bool,
        cert_file: Optional[str] = None,
        key_file: Optional[str] = None,
        ca_file: Optional[str] = None,
    ):
        """
        Initializes the TCPServer.

        Args:
            host (str): The host address.
            port (int): The port number.
            use_tls (bool): Whether to use TLS.
            cert_file (str): Path to the certificate file.
            key_file (str): Path to the key file.
            ca_file (str): Path to the CA file.
        """
        super().__init__()
        self.host: str = host
        self.port: int = port
        self.use_tls: bool = use_tls
        self.cert_file: str | None = cert_file
        self.key_file: str | None = key_file
        self.ca_file: str | None= ca_file
        self._transaction_id: int | None = None
        self._unit_id: int | None = None

    async def start(self):
        """
        Starts the TCP server.
        """
        addr = f"{self.host}:{self.port}"
        if self.use_tls:
            if self.cert_file is None or self.key_file is None:
                raise ValueError("TLS is enabled but no certificate or key file is provided.")
            ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            ssl_context.load_cert_chain(certfile=self.cert_file, keyfile=self.key_file)
            if self.ca_file:
                ssl_context.load_verify_locations(self.ca_file)
                ssl_context.verify_mode = ssl.CERT_REQUIRED
            server = await asyncio.start_server(
                self.handle_connection, self.host, self.port, ssl=ssl_context
            )
        else:
            server = await asyncio.start_server(
                self.handle_connection, self.host, self.port
            )

        async with server:
            await server.serve_forever()

    async def parse_adu(self, data: bytes) -> TCPADU:
        """
        Parses the Application Data Unit (ADU).

        Args:
            data (bytes): The raw data to parse.

        Returns:
            TCPADU: The parsed ADU.
        """
        try:
            tcp_adu = TCPADU()
            tcp_adu.from_bytes(data)
            self._transaction_id = tcp_adu.transaction_id
            self._unit_id = tcp_adu.unit_id
            return tcp_adu
        except Exception as e:
            raise ValueError(f"Failed to parse ADU: {e}")

    async def pack_adu(
        self,
        pdu: (
            PDUErrorResponse
            | PDUReadResponse
            | PDUWriteSingleResponse
            | PDUWriteMultipleResponse
        ),
    ) -> TCPADU:
        """
        Packs the Protocol Data Unit (PDU) into an ADU.

        Args:
            pdu (PDUErrorResponse | PDUReadResponse | PDUWriteSingleResponse | PDUWriteMultipleResponse): The PDU to pack.

        Returns:
            TCPADU: The packed ADU.
        """
        try:
            tcp_adu = TCPADU(
                transaction_id=self._transaction_id,
                unit_id=self._unit_id,
                pdu=pdu.to_bytes(),
            )
            self._transaction_id = None
            self._unit_id = None
            return tcp_adu
        except Exception as e:
            raise ValueError(f"Failed to pack ADU: {e}")
