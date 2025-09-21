from textwrap import dedent
from schema import Device
from settings import Settings


def print_wireguard_config(settings: Settings, device: Device) -> str:
    return dedent(
        f"""\
        [Interface]
        PrivateKey = {device.private_key}
        Address = {device.address}
        DNS = 8.8.8.8, 8.8.4.4

        [Peer]
        Endpoint = {settings.public_host}:{settings.public_port}
        PublicKey = {settings.wg_public_key}
        AllowedIPs = 0.0.0.0/0
    """
    )
