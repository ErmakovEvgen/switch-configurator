from enum import Enum

from app.models.client import ClientConfig


class Scenario(str, Enum):
    NORMAL = "normal"
    IP = "ip"
    RING = "ring"


def detect_scenario(config: ClientConfig) -> Scenario:
    if config.ring_switch is not None:
        if config.ip is not None or config.vlan is not None:
            raise ValueError(
                "Для режима кольца IP и VLAN не должны быть указаны"
            )

        return Scenario.RING

    if config.ip is not None:
        if config.vlan is None:
            raise ValueError(
                "Для клиента с IP необходимо указать VLAN"
            )

        return Scenario.IP

    if config.vlan is None:
        raise ValueError(
            "Необходимо указать VLAN или коммутатор в кольце"
        )

    return Scenario.NORMAL