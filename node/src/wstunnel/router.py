from fastapi import APIRouter
from typing import Literal

from fastapi import Depends, HTTPException

from ..state import State, get_global_state
from ..auth import verify_token
from .models import WsTunnelClientConfig, WsTunnelServerConfig
from .tunnel import WebSocketTunnel

router = APIRouter(tags=["Wstunnel"])


@router.get("/wstunnel")
async def get_wstunnel_config(
    state: State = Depends(get_global_state), _: None = Depends(verify_token)
) -> WsTunnelClientConfig | WsTunnelServerConfig:
    if state.wstunnel is None:
        raise HTTPException(status_code=404, detail="No configuration set")
    return state.wstunnel.config


@router.put("/wstunnel")
async def start_wstunnel(
    config: WsTunnelClientConfig | WsTunnelServerConfig,
    state: State = Depends(get_global_state),
    _: None = Depends(verify_token),
) -> Literal["Ok"]:
    if state.wstunnel is not None:
        state.wstunnel.stop()
    state.wstunnel = WebSocketTunnel(config)
    state.wstunnel.start()
    return "Ok"


@router.delete("/wstunnel")
async def stop_wstunnel(
    state: State = Depends(get_global_state), _: None = Depends(verify_token)
) -> Literal["Ok"]:
    if state.wstunnel is None:
        return "Ok"
    state.wstunnel.stop()
    state.wstunnel = None
    return "Ok"
