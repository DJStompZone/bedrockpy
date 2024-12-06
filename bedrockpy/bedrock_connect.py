import socket
import logging

from parser import PacketParser
from colorama import init, Fore, Style
import re

init(autoreset=True)

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(message)s",
    datefmt="%H:%M:%S",
)

MC_COLOR_MAP = {
    "0": Fore.BLACK,
    "1": Fore.BLUE,
    "2": Fore.GREEN,
    "3": Fore.CYAN,
    "4": Fore.RED,
    "5": Fore.MAGENTA,
    "6": Fore.YELLOW,
    "7": Fore.WHITE,
    "8": Fore.LIGHTBLACK_EX,
    "9": Fore.LIGHTBLUE_EX,
    "a": Fore.LIGHTGREEN_EX,
    "b": Fore.LIGHTCYAN_EX,
    "c": Fore.LIGHTRED_EX,
    "d": Fore.LIGHTMAGENTA_EX,
    "e": Fore.LIGHTYELLOW_EX,
    "f": Fore.RESET,
}

def colorize_minecraft_text(text):
    """
    Converts Minecraft § color codes into colorama styles.
    """
    def replacer(match):
        color_code = match.group(1).lower()
        return MC_COLOR_MAP.get(color_code, "")

    return re.sub(r"§([0-9a-f])", replacer, text) + Style.RESET_ALL

def send_packet(sock, server_address, packet, packet_name="Packet"):
    """
    Sends a packet to the server and returns the response.
    """
    try:
        logging.debug(f"{Fore.CYAN}Sending {packet_name}: {packet.hex()}")
        sock.sendto(packet, server_address)
        logging.info(f"{Fore.GREEN}{packet_name} sent to {server_address}.")
        response, addr = sock.recvfrom(2048)
        logging.debug(f"{Fore.CYAN}Received raw response: {response.hex()} from {addr}.")
        return response
    except Exception as e:
        logging.error(f"{Fore.RED}Error while sending {packet_name}: {e}")
        raise

def display_response(response):
    """
    Displays the parsed response in a formatted and colorized way.
    """
    logging.info(f"\n{Style.BRIGHT}{Fore.YELLOW}=== Unconnected Pong Response ===")
    for key, value in response.items():
        if isinstance(value, str) and "§" in value:
            value = colorize_minecraft_text(value)
        logging.info(f"{Fore.CYAN}{key}: {Fore.WHITE}{value}")

def connect(SERVER_HOST="mc.tectonix.win", SERVER_PORT=19132, timeout=10):
    """
    Establishes a connection to the specified server and displays responses.
    """
    server_address = (SERVER_HOST, SERVER_PORT)
    parser = PacketParser()
    parser.load_plugins()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(timeout)

    try:
        unconnected_ping_packet = parser.packet_handlers[0x01].encode()
        response = send_packet(sock, server_address, unconnected_ping_packet, "Unconnected Ping")
        server_info = parser.parse_packet(0x1C, response)
        if server_info:
            logging.info(f"{Fore.GREEN}Successfully decoded Unconnected Pong response.")
            display_response(server_info)

        mtu = 1200
        open_conn_req_1_packet = parser.packet_handlers[0x05].encode(mtu)
        response = send_packet(sock, server_address, open_conn_req_1_packet, "Open Connection Request 1")
        conn_reply_1_info = parser.parse_packet(0x06, response)
        if conn_reply_1_info:
            logging.info(f"{Fore.GREEN}Successfully decoded Open Connection Reply 1.")
            logging.info(f"{Style.BRIGHT}{Fore.YELLOW}=== Open Connection Reply 1 ===")
            for key, value in conn_reply_1_info.items():
                logging.info(f"{Fore.CYAN}{key}: {Fore.WHITE}{value}")

        logging.info(f"{Fore.GREEN}Connection established up to Open Connection Reply 1.")
        logging.info(f"{Fore.YELLOW}Additional steps (Open Connection Request 2) are required for full connection.")

    except socket.timeout:
        logging.error(f"{Fore.RED}Server did not respond. It might be offline or unreachable.")
    except Exception as e:
        logging.critical(f"{Fore.RED}Unexpected error: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    connect()
