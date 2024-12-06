from packets.base import BasePacket

class ConnectedPong(BasePacket):
    packet_id = 0x03

    @staticmethod
    def decode(data: bytes) -> dict:
        """
        Decodes the Connected Pong packet.
        """
        try:
            server_timestamp = int.from_bytes(data[1:9], "big")
            client_timestamp = int.from_bytes(data[9:17], "big")
            return {
                "server_timestamp": server_timestamp,
                "client_timestamp": client_timestamp,
                "latency_ms": (server_timestamp - client_timestamp) / 1000,
            }
        except (ValueError, IndexError) as e:
            raise ValueError(f"Failed to decode Connected Pong packet: {e}")
