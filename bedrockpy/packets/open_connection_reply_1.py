from packets.base import BasePacket

class OpenConnectionReply1(BasePacket):
    packet_id = 0x06

    @staticmethod
    def decode(data: bytes) -> dict:
        """
        Decodes the Open Connection Reply 1 packet.
        """
        try:
            server_guid = int.from_bytes(data[1:9], "big")
            mtu_size = int.from_bytes(data[9:11], "big")
            return {
                "server_guid": server_guid,
                "mtu_size": mtu_size,
            }
        except (ValueError, IndexError) as e:
            raise ValueError(f"Failed to decode Open Connection Reply 1 packet: {e}")
