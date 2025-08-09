import subprocess
from settings import Settings
from wg_server import INTERNAL_PORT


def start_wstunnel_server(settings: Settings):
    subprocess.run(
        [
            "wstunnel",
            "server",
            "--restrict-http-upgrade-path-prefix",
            settings.ws_password,
            "--restrict-to",
            f"localhost:{INTERNAL_PORT}",
            f"wss://0.0.0.0:{settings.ws_port}",
        ],
        check=True,
    )
