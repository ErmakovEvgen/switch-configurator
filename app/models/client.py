from ipaddress import IPv4Address

from pydantic import BaseModel, Field


class ClientConfig(BaseModel):
    fio: str = Field(min_length=3)
    apartment: int = Field(ge=1)
    port: int = Field(ge=1)
    vlan: int | None = Field(default=None, ge=1, le=4094)
    ip: IPv4Address | None = None
    ring_switch: int | None = Field(default=None, ge=1)
    iptv: bool = False