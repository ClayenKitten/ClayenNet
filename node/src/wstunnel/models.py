from ipaddress import IPv4Address
from typing import Literal

from pydantic import BaseModel, Field

class WsTunnelClientConfig(BaseModel):
    kind: Literal["client"]
    address: IPv4Address
    password: str

class WsTunnelServerConfig(BaseModel):
    kind: Literal["server"]
    password: str = Field(min_length=8)
