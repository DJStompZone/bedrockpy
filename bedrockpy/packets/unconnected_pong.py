from packets.base import BasePacket

class UnconnectedPong(BasePacket):
    packet_id = 0x1C

    @staticmethod
    def decode(data: bytes) -> dict:
        """
        Decodes the Unconnected Pong packet.
        """
        try:
            server_guid = int.from_bytes(data[1:9], "big")

            magic_index = data.find(b"\x00\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd")
            if magic_index == -1:
                raise ValueError("Magic bytes not found in Unconnected Pong packet.")

            payload_start = magic_index + 16
            payload = data[payload_start:]

            decoded_payload = payload.decode("utf-8", errors="replace")
            fields = decoded_payload.split(";")

            return {
                "server_guid": server_guid,
                "protocol": fields[0],
                "server_name": fields[1],
                "protocol_version": int(fields[2]),
                "game_version": fields[3],
                "current_players": int(fields[4]),
                "max_players": int(fields[5]),
                "server_id": fields[6],
                "motd": fields[7],
                "game_mode": fields[8],
                "port_ipv4": int(fields[10]),
                "port_ipv6": int(fields[11]),
            }
        except (ValueError, IndexError, UnicodeDecodeError) as e:
            raise ValueError(f"Failed to decode Unconnected Pong packet: {e}")
