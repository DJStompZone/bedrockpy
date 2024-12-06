import click
from parser import PacketParser

@click.group()
def cli():
    """Minecraft Bedrock Protocol Parser CLI."""
    pass

@cli.command()
@click.argument("packet_type", type=str)
@click.option("--data", type=str, help="Raw packet data in hexadecimal for decoding.")
@click.option("--args", type=str, help="Arguments for encoding, as a JSON string.")
def parse(packet_type, data, args):
    """
    Parses or encodes a packet dynamically.
    """
    parser = PacketParser()
    parser.load_plugins()

    if packet_type not in parser.packet_handlers:
        click.echo(f"Error: No handler registered for packet type '{packet_type}'")
        return

    packet_class = parser.packet_handlers[packet_type]

    if data:
        raw_data = bytes.fromhex(data)
        result = packet_class.decode(raw_data)
        click.echo(f"Decoded Packet: {result}")
    elif args:
        import json
        kwargs = json.loads(args)
        packet = packet_class.encode(**kwargs)
        click.echo(f"Encoded Packet: {packet.hex()}")
    else:
        click.echo("Error: Provide either --data or --args.")

if __name__ == "__main__":
    cli()
