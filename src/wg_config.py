from textwrap import dedent
from schema import Device
from settings import Settings


def print_wireguard_config(settings: Settings, device: Device) -> str:
    return dedent(
        f"""\
        [Interface]
        PrivateKey={device.private_key}
        Address={device.address}

        [Peer]
        Endpoint={settings.public_host}:{settings.public_port}
        PublicKey={settings.wg_public_key}
        AllowedIPs={', '.join(allowed_ips)}
    """
    )


# AllowedIPs calculated to skip 192.168.0.0/16 and 172.16.0.0/12 networks
# Generated via https://www.procustodibus.com/blog/2021/03/wireguard-allowedips-calculator/
allowed_ips = [
    "0.0.0.0/1",
    "128.0.0.0/3",
    "160.0.0.0/5",
    "168.0.0.0/6",
    "172.0.0.0/12",
    "172.32.0.0/11",
    "172.64.0.0/10",
    "172.128.0.0/9",
    "173.0.0.0/8",
    "174.0.0.0/7",
    "176.0.0.0/4",
    "192.0.0.0/9",
    "192.128.0.0/11",
    "192.160.0.0/13",
    "192.169.0.0/16",
    "192.170.0.0/15",
    "192.172.0.0/14",
    "192.176.0.0/12",
    "192.192.0.0/10",
    "193.0.0.0/8",
    "194.0.0.0/7",
    "196.0.0.0/6",
    "200.0.0.0/5",
    "208.0.0.0/4",
    "224.0.0.0/3",
]
