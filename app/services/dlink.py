from app.models.client import ClientConfig
from app.services.scenario import Scenario
from app.services.values import get_access_vlan, get_description


class DLinkGenerator:

    def generate(
        self,
        config: ClientConfig,
        scenario: Scenario,
    ) -> str:

        if scenario == Scenario.RING:
            return self._ring(config)

        if scenario == Scenario.NORMAL:
            return self._normal(config)

        # Excel не формирует D-Link-конфигурацию
        # для клиента с IP.
        return ""

    # =====================================================
    # Обычный клиент
    # Excel: H4:H53
    # =====================================================

    def _normal(
        self,
        config: ClientConfig,
    ) -> str:

        if config.vlan is None:
            raise ValueError(
                "Для D-Link необходимо указать VLAN"
            )

        port = config.port
        vlan = config.vlan
        description = get_description(config)

        commands = [

            # H24
            "en ad",

            # H25
            "edding345",

            # H26
            "enable dhcp_local_relay",

            # H27
            "enable address_binding dhcp_snoop",

            # H28
            f"config port_security ports {port} admin_state disable",

            # H29
            f"config dhcp_local_relay option_82 ports {port} policy replace",

            # H30
            f"config address_binding ip_mac ports {port} state enable loose",

            # H31
            f"config address_binding ip_mac ports {port} arp_inspection disable",

            # H32
            f"config address_binding ip_mac ports {port} ip_inspection enable",

            # H33
            f"config address_binding ip_mac ports {port} allow_zeroip enable",

            # H34
            f"config address_binding ip_mac ports {port} stop_learning_threshold 5",

            # H35
            f"config address_binding ip_mac ports {port} forward_dhcppkt enable",

            # H36
            f"config filter dhcp_server ports {port} state enable",

            # H37
            f"config ports {port} state enable",

            # H38
            f"config ports {port} description {description}_kv{config.apartment}",

            # H39
            f"config access_profile profile_id 2 delete access_id {100 + port}",

            # H40
            f"config access_profile profile_id 2 delete access_id {200 + port}",

            # H41
            f"config access_profile profile_id 7 delete access_id {port}",

            # H42
            f"config access_profile profile_id 8 delete access_id {port}",

            # H43
            f"config access_profile profile_id 9 delete access_id {port}",

            # H44
            f"config access_profile profile_name 2 delete access_id {100 + port}",

            # H45
            f"config access_profile profile_name 2 delete access_id {200 + port}",

            # H46
            f"config access_profile profile_name 7 delete access_id {100 + port}",

            # H47
            f"config access_profile profile_name 7 delete access_id {200 + port}",

            # H48
            f"config access_profile profile_name 9 delete access_id {100 + port}",

            # H49
            f"config access_profile profile_name 9 delete access_id {200 + port}",

            # H50
            f"config vlan vlanid {vlan} add untagged {port}",

            # H51
            f"config dhcp_local_relay vlan vlanid {vlan} state enable",

            # H52
            f"config bandwidth_control {port} rx_rate no_limit tx_rate no_limit ",

            # H53
            "save",
        ]

        return "\n".join(commands)

    # =====================================================
    # Клиент в кольце
    # Excel: D34:D57
    # =====================================================

    def _ring(
        self,
        config: ClientConfig,
    ) -> str:

        if config.ring_switch is None:
            raise ValueError(
                "Для D-Link в кольце необходимо указать "
                "номер коммутатора"
            )

        port = config.port
        vlan = get_access_vlan(
            config,
            Scenario.RING,
        )

        description = get_description(config)

        commands = [
            # D34
            f"config ports {port} state enable",

            # D35
            f"config ports {port} description {config.fio}_kv{config.apartment}",

            # D36
            f"config port_security ports {port} admin_state disable",

            # D37
            f"config address_binding ip_mac ports {port} state enable loose",

            # D38
            f"config address_binding ip_mac ports {port} arp_inspection loose",

            # D39
            f"config address_binding ip_mac ports {port} ip_inspection enable",

            # D40
            f"config address_binding ip_mac ports {port} allow_zeroip enable",

            # D41
            f"config address_binding ip_mac ports {port} stop_learning_threshold 5",

            # D42
            f"config address_binding ip_mac ports {port} forward_dhcppkt enable",

            # D43
            f"config filter dhcp_server ports {port} state enable",

            # D44
            f"config access_profile profile_id 2 delete access_id {100 + port}",

            # D45
            f"config access_profile profile_id 2 delete access_id {200 + port}",

            # D46
            f"config access_profile profile_id 7 delete access_id {port}",

            # D47
            f"config access_profile profile_id 8 delete access_id {port}",

            # D48
            f"config access_profile profile_id 9 delete access_id {port}",

            # D49
            f"config access_profile profile_name 7 delete access_id {100 + port}",

            # D50
            f"config access_profile profile_name 9 delete access_id {200 + port}",

            # D51
            f"config access_profile profile_name 2 delete access_id {100 + port}",

            # D52
            f"config access_profile profile_name 2 delete access_id {200 + port}",

            # D53
            f"config igmp_snooping multicast_vlan IP_TV add member_port {port}",

            # D54
            f"config igmp_snooping multicast_vlan 56 add member_port {port}",

            # D55
            f"config vlan vlanid {vlan} add untagged {port}",

            # D56
            f"config bandwidth_control {port} rx_rate no_limit tx_rate no_limit ",

            # D57
            "save",
        ]

        return "\n".join(commands)