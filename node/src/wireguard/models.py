from datetime import datetime
import subprocess
from pydantic import BaseModel, Field
from ipaddress import IPv4Network


class Peer(BaseModel):
    name: str
    public_key: str = Field(min_length=1)
    endpoint: str | None = Field(min_length=1, default=None)
    allowed_ips: list[IPv4Network]


class WireguardPeerMetric(BaseModel):
    """Metrics about WireGuard connection"""

    name: str
    latest_handshake: datetime
    transfer_rx: int
    transfer_tx: int


class WireguardConfig(BaseModel):
    """WireGuard configuration in structured format."""

    address: IPv4Network
    private_key: str = Field(min_length=3)
    peers: list[Peer] = []


class WireguardInterface(BaseModel):
    """WireGuard network interface."""

    interface_name: str
    address: IPv4Network
    private_key: str = Field(min_length=3)
    peers: list[Peer] = []

    def apply(self):
        """Create and configure network interface."""
        subprocess.run(["ip", "link", "del", self.interface_name])
        subprocess.run(
            ["ip", "link", "add", self.interface_name, "type", "wireguard"], check=True
        )
        subprocess.run(
            ["ip", "addr", "add", str(self.address), "dev", self.interface_name],
            check=True,
        )
        subprocess.run(
            f'bash -c "wg set {self.interface_name} listen-port 51820 private-key <(echo $PRIVATE_KEY)"',
            env={"PRIVATE_KEY": self.private_key},
            check=True,
            shell=True,
        )
        subprocess.run(["ip", "link", "set", self.interface_name, "up"], check=True)
        for peer in self.peers:
            args = [
                "wg",
                "set",
                self.interface_name,
                "peer",
                peer.public_key,
                "allowed-ips",
                ",".join([str(ip) for ip in peer.allowed_ips]),
            ]
            if peer.endpoint is not None:
                args.extend(["endpoint", peer.endpoint])
            subprocess.run(args, check=True)
            for ip in peer.allowed_ips:
                subprocess.run(
                    ["ip", "route", "add", str(ip), "dev", self.interface_name],
                    check=True,
                )

    def remove(self):
        """Remove network interface."""
        subprocess.run(["ip", "link", "del", self.interface_name])

    def get_config(self) -> WireguardConfig:
        """Returns structured config"""
        return WireguardConfig(
            address=self.address, private_key=self.private_key, peers=self.peers
        )

    def find_peer_by_public_key(self, public_key: str) -> Peer | None:
        """Find and return peer by public key."""
        return next(
            filter(lambda peer: peer.public_key == public_key, self.peers), None
        )
