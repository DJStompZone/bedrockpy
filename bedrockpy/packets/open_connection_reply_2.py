from packets.base import BasePacket

class OpenConnectionReply2(BasePacket):
    packet_id = 0x08

    @staticmethod
    def decode(data: bytes) -> dict:
        """
        Decodes the Open Connection Reply 2 packet.

        :param data: Raw response data.
        :return: Parsed response as a dictionary.
        """
        try:
            server_guid = int.from_bytes(data[1:9], "big")
            use_encryption = bool(data[9])
            mtu_size = int.from_bytes(data[10:12], "big")

            return {
                "server_guid": server_guid,
                "use_encryption": use_encryption,
                "mtu_size": mtu_size,
            }
        except (IndexError, ValueError) as e:
            raise ValueError(f"Failed to decode Open Connection Reply 2 packet: {e}")
