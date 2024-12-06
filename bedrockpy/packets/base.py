import logging
from colorama import Fore

class BasePacket:
    packet_id = None

    @staticmethod
    def encode(*args, **kwargs) -> bytes:
        raise NotImplementedError("Encode method must be implemented.")

    @staticmethod
    def decode(data: bytes) -> dict:
        raise NotImplementedError("Decode method must be implemented.")

    @classmethod
    def safe_decode(cls, data: bytes) -> dict:
        """
        Safely decodes a packet, logging errors and returning None on failure.
        """
        try:
            return cls.decode(data)
        except Exception as e:
            logging.error(f"{Fore.RED}Failed to decode {cls.__name__} packet: {e}")
            logging.debug(f"{Fore.CYAN}Raw response: {data.hex()}")
            return None
