from app.models.client import ClientConfig
from app.services.scenario import Scenario
from app.services.values import (
    get_access_vlan,
    get_acl_number,
    get_description,
)


class CiscoGenerator:

    def generate(
        self,
        config: ClientConfig,
        scenario: Scenario,
    ) -> str:

        commands: list[str] = []

        # Строки 4-22 Excel
        commands.extend(
            self._common_commands(config)
        )

        # Строка 23 Excel
        # Description есть ТОЛЬКО если:
        # IP отсутствует и коммутатор кольца отсутствует.
        if (
            config.ip is None
            and config.ring_switch is None
        ):
            commands.append(
                self._description(config)
            )

        # Строка 24 Excel
        commands.append(
            self._access_vlan(config, scenario)
        )

        # Строка 25 Excel
        # Только IP-клиент.
        if scenario == Scenario.IP:
            commands.append(
                self._ip_access_group(config)
            )

        # Строки 26-27 Excel
        if config.iptv:
            commands.extend(
                self._iptv_commands()
            )

        # Строка 28 Excel
        commands.append("exit")

        # Строки 29-32 Excel
        if scenario == Scenario.IP:
            commands.extend(
                self._ip_acl(config)
            )

        # Строки 33-34 Excel
        commands.extend([
            "end",
            "wr mem",
        ])

        return "\n".join(commands)

    # =====================================================
    # Строки 4-22
    # =====================================================

    def _common_commands(
        self,
        config: ClientConfig,
    ) -> list[str]:

        return [
            "conf t",
            f"default interface fa0/{config.port}",
            f"int fa0/{config.port}",
            "no shutdown",
            "switchport mode access",
            "switchport protected",
            "switchport port-security",
            "switchport port-security maximum 1",
            "switchport port-security aging time 1",
            "switchport port-security violation protect",
            "no ip address",
            "storm-control broadcast level pps 128 128",
            "storm-control multicast level pps 128 128",
            "ip dhcp snooping limit rate 5",

            # Excel F18 — это не формула,
            # строка присутствует непосредственно в таблице.
            "storm-control action shutdown",

            "no cdp enable",
            "spanning-tree bpduguard enable",
            "spanning-tree guard root",
            "spanning-tree portfast",
        ]

    # =====================================================
    # Строка 23
    # =====================================================

    def _description(
        self,
        config: ClientConfig,
    ) -> str:

        description = get_description(config)

        return (
            f"description "
            f"{description}_kv{config.apartment}"
        )

    # =====================================================
    # Строка 24
    # =====================================================

    def _access_vlan(
        self,
        config: ClientConfig,
        scenario: Scenario,
    ) -> str:

        vlan = get_access_vlan(
            config,
            scenario,
        )

        return (
            f"switchport access vlan {vlan}"
        )

    # =====================================================
    # Строка 25
    # =====================================================

    def _ip_access_group(
        self,
        config: ClientConfig,
    ) -> str:

        acl = get_acl_number(config)

        return (
            f"ip access-group {acl} in"
        )

    # =====================================================
    # Строки 26-27
    # =====================================================

    def _iptv_commands(self) -> list[str]:

        return [
            "mvr type receiver",
            "mvr immediate",
        ]

    # =====================================================
    # Строки 29-32
    # =====================================================

    def _ip_acl(
        self,
        config: ClientConfig,
    ) -> list[str]:

        if config.ip is None:
            raise ValueError(
                "Для IP-клиента IP-адрес должен быть указан"
            )

        acl = get_acl_number(config)

        return [
            f"no access-list {acl}",
            (
                f"access-list {acl} "
                f"remark {config.fio}_kv{config.apartment}"
            ),
            (
                f"access-list {acl} "
                f"permit ip host {config.ip} any"
            ),
            (
                f"access-list {acl} "
                f"deny   ip any any"
            ),
        ]