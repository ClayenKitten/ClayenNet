from datetime import timezone, datetime
import subprocess
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException

from ..state import State, get_global_state
from ..config import Configuration
from ..auth import verify_token
from .models import WireguardConfig, WireguardInterface, WireguardPeerMetric

router = APIRouter()


@router.get("/wireguard", tags=["WireGuard"])
async def get_wireguard_config(
    state: State = Depends(get_global_state), _: None = Depends(verify_token)
) -> WireguardConfig:
    if state.wireguard is None:
        raise HTTPException(status_code=404, detail="No configuration set")
    return state.wireguard.get_config()


@router.get("/wireguard/metrics", tags=["WireGuard"])
async def get_wireguard_metrics(
    state: State = Depends(get_global_state),
    app_config: Configuration = Depends(),
    _: None = Depends(verify_token),
) -> list[WireguardPeerMetric]:
    if state.wireguard is None:
        raise HTTPException(status_code=404, detail="No configuration set")

    str_result = subprocess.run(
        ["wg", "show", app_config.wireguard_interface],
        check=True,
        capture_output=True,
        text=True,
    ).stdout

    peerMetrics: list[WireguardPeerMetric] = []
    for i, line in enumerate(str_result.split("\n")):
        if i == 0:
            continue
        fields = line.split(" ")

        peer = state.wireguard.find_peer_by_public_key(fields[0])
        if peer is None: continue

        peerMetrics.append(
            WireguardPeerMetric(
                name=peer.name,
                latest_handshake=datetime.fromtimestamp(int(fields[4]), timezone.utc),
                transfer_rx=int(fields[5]),
                transfer_tx=int(fields[6]),
            )
        )
    return peerMetrics


@router.put("/wireguard", tags=["WireGuard"])
async def start_wireguard(
    config: WireguardConfig,
    state: State = Depends(get_global_state),
    app_config: Configuration = Depends(),
    _: None = Depends(verify_token),
) -> WireguardConfig:
    interface = WireguardInterface(
        interface_name=app_config.wg_interface,
        address=config.address,
        peers=config.peers,
        private_key=config.private_key
    )
    try:
        if state.wireguard is not None:
            state.wireguard.remove()
            state.wireguard = None
        interface.apply()
        state.wireguard = interface
    except subprocess.CalledProcessError as e:
        # Cleanup
        subprocess.run(
            ["ip", "link", "del", app_config.wireguard_interface],
            stderr=subprocess.DEVNULL,
        )
        print(e.output)
        raise HTTPException(
            status_code=500, detail=f"Failed to apply WireGuard config: {e}"
        )
    return interface.get_config()


@router.delete("/wireguard", tags=["WireGuard"])
async def stop_wireguard(
    state: State = Depends(get_global_state), _: None = Depends(verify_token)
) -> Literal["Ok"]:
    if state.wireguard is None:
        return "Ok"
    state.wireguard.remove()
    state.wireguard = None
    return "Ok"
