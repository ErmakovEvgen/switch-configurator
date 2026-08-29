from app.models.client import ClientConfig
from app.services.scenario import Scenario
from app.utils.transliteration import fio_to_description


def get_description(config: ClientConfig) -> str:
    """
    Описание порта в формате Excel:
    Фамилия + первая буква имени + первая буква отчества.

    Например:
    Абназыров Рустам Абдульфаритович
    -> AbnazyrovRA
    """
    return fio_to_description(config.fio)


def get_ring_vlan(config: ClientConfig) -> int:
    """
    Расчёт VLAN для режима коммутатора в кольце.

    Excel:
    3000 + B12 + B14 * 50 - 50
    """
    if config.ring_switch is None:
        raise ValueError(
            "Номер коммутатора в кольце не указан"
        )

    return (
        3000
        + config.port
        + config.ring_switch * 50
        - 50
    )


def get_access_vlan(
    config: ClientConfig,
    scenario: Scenario,
) -> int:
    """
    VLAN, который должен попасть в Cisco-конфигурацию.

    Для обычного/IP-клиента:
        используется введённый VLAN.

    Для кольца:
        используется расчётный VLAN.
    """
    if scenario == Scenario.RING:
        return get_ring_vlan(config)

    if config.vlan is None:
        raise ValueError("VLAN не указан")

    return config.vlan


def get_acl_number(config: ClientConfig) -> int:
    """
    Номер ACL для клиента с IP.

    Excel:
    B12 + 100
    """
    return config.port + 100