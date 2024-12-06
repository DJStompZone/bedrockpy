from packets.base import BasePacket
import time

class UnconnectedPing(BasePacket):
    packet_id = 0x01

    @staticmethod
    def encode() -> bytes:
        """
        Encodes the Unconnected Ping packet.
        """
        timestamp = int(time.time_ns() // 1_000_000).to_bytes(8, "big")
        magic = b"\x00\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x12\x34\x56\x78"
        return b"\x01" + timestamp + magic
