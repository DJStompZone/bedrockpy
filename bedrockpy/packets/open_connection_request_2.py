from packets.base import BasePacket
import os

class OpenConnectionRequest2(BasePacket):
    packet_id = 0x07

    @staticmethod
    def encode(server_guid: int, mtu_size: int, client_guid: int = None) -> bytes:
        """
        Encodes the Open Connection Request 2 packet.

        :param server_guid: Server's GUID from Reply 1.
        :param mtu_size: MTU size from Reply 1.
        :param client_guid: Client GUID (randomly generated if not provided).
        :return: Encoded packet as bytes.
        """
        if client_guid is None:
            client_guid = int.from_bytes(os.urandom(8), "big")

        magic = b"\x00\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x12\x34\x56\x78"
        return (
            b"\x07"
            + magic
            + server_guid.to_bytes(8, "big")
            + mtu_size.to_bytes(2, "big")
            + client_guid.to_bytes(8, "big")
        )
