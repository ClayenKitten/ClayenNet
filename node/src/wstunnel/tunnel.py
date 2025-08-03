from .models import WsTunnelClientConfig, WsTunnelServerConfig

from subprocess import Popen, run

class WebSocketTunnel:
    """Tunnel over WebSocket protocol."""

    def __init__(self, config: WsTunnelClientConfig | WsTunnelServerConfig):
        self.config = config

    process: Popen | None = None

    def start(self):
        """Start the tunnel."""
        if self.config.kind == "client":
            run(
                ["ip", "route", "add", f"{str(self.config.address)}/32", "dev", "eth0"],
                check=True
            )
            self.process = Popen([
                "wstunnel", "client",
                "--http-upgrade-path-prefix", self.config.password,
                "-L", "udp://51820:localhost:51820?timeout_sec=0",
                f"wss://{str(self.config.address)}:443"
            ])
        else:
            self.process = Popen([
                "wstunnel", "server",
                "--restrict-http-upgrade-path-prefix", self.config.password,
                "--restrict-to", "localhost:51820",
                "wss://0.0.0.0:443"
            ])

    def stop(self):
        """Stop the tunnel."""
        if self.config.kind == "client":
            run(
                ["ip", "route", "del", f"{str(self.config.address)}/32", "dev", "eth0"],
                check=False
            )
        if self.process:
            self.process.terminate()
        else:
            pass
