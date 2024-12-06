from packets.base import BasePacket
import time

class ConnectedPing(BasePacket):
    packet_id = 0x00

    @staticmethod
    def encode() -> bytes:
        """
        Encodes the Connected Ping packet.
        """
        timestamp = int(time.time_ns() // 1_000_000).to_bytes(8, "big")
        return b"\x00" + timestamp
