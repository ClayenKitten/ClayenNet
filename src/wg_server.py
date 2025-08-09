import subprocess

from sqlalchemy import select
from sqlalchemy.orm import Session

from schema import Device
from settings import Settings

INTERNAL_PORT = 9000


def start_wg_server(settings: Settings, session: Session):
    subprocess.run(["ip", "link", "del", "wg0"])
    subprocess.run(["ip", "link", "add", "wg0", "type", "wireguard"], check=True)
    subprocess.run(
        ["ip", "addr", "add", settings.wg_address, "dev", "wg0"],
        check=True,
    )
    subprocess.run(
        f'bash -c "wg set wg0 listen-port {INTERNAL_PORT} private-key <(echo $PRIVATE_KEY)"',
        env={"PRIVATE_KEY": settings.wg_private_key},
        check=True,
        shell=True,
    )
    subprocess.run(["ip", "link", "set", "wg0", "up"], check=True)

    for device in session.execute(select(Device)).scalars():
        subprocess.run(
            [
                "wg",
                "set",
                "wg0",
                "peer",
                device.public_key,
                "allowed-ips",
                device.address,
            ],
            check=True,
        )
        subprocess.run(
            ["ip", "route", "add", device.address, "dev", "wg0"],
            check=True,
        )
