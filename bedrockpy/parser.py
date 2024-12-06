import os
import importlib.util
import logging
from packets.base import BasePacket

class PacketParser:
    def __init__(self):
        self.packet_handlers = {}

    def load_plugins(self, plugin_dir="packets"):
        """
        Dynamically loads packet plugins from the specified directory.
        """
        for filename in os.listdir(plugin_dir):
            if filename.endswith(".py") and filename != "base.py" and filename != "__init__.py":
                module_name = f"{plugin_dir}.{filename[:-3]}"
                spec = importlib.util.spec_from_file_location(module_name, os.path.join(plugin_dir, filename))
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                for attr in dir(module):
                    cls = getattr(module, attr)
                    if isinstance(cls, type) and issubclass(cls, BasePacket) and cls is not BasePacket:
                        self.register_packet(cls)

    def register_packet(self, packet_class):
        """
        Registers a packet class with the parser.
        """
        if packet_class.packet_id is None:
            logging.warning(f"Skipping {packet_class.__name__}: No packet_id defined.")
            return
        self.packet_handlers[packet_class.packet_id] = packet_class
        logging.info(f"Registered {packet_class.__name__} with packet_id {packet_class.packet_id}.")

    def parse_packet(self, packet_id, data):
        """
        Parses a packet using the appropriate handler.
        """
        if packet_id not in self.packet_handlers:
            raise ValueError(f"No handler registered for packet ID {packet_id}.")
        handler = self.packet_handlers[packet_id]
        return handler.safe_decode(data)
