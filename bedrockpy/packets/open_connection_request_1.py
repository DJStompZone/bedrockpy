from packets.base import BasePacket

class OpenConnectionRequest1(BasePacket):
    packet_id = 0x05

    @staticmethod
    def encode(mtu: int = 1200) -> bytes:
        """
        Encodes the Open Connection Request 1 packet.
        """
        magic = b"\x00\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x12\x34\x56\x78"
        return b"\x05" + magic + mtu.to_bytes(2, "big")
