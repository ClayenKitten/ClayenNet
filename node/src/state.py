from dataclasses import dataclass
from typing import Optional

from .wireguard.models import WireguardInterface
from .wstunnel.tunnel import WebSocketTunnel

@dataclass
class State:
    wireguard: Optional[WireguardInterface] = None
    wstunnel: Optional[WebSocketTunnel] = None

state = State()

def get_global_state() -> State:
    print(state)
    return state
