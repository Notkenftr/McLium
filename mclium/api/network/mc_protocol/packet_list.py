from mclium.api.network.mc_protocol.packet_builder import PacketBuilder, _Field
from mclium.api.network.mc_protocol.packet_builder import PacketFieldType
class PacketList:
    """
    ServerBound packet list
    """

    @staticmethod
    def get_handshake_state(protocol, address, port, state=1, debug=False):
        """
        :param state: state 1 = get server status, state 2 = login request
        :return: packet.Build()
        """
        packet = PacketBuilder(0x00, debug)

        packet.add_field(_Field(PacketFieldType.VARINT, int(protocol)))
        packet.add_field(_Field(PacketFieldType.STRING, str(address)))
        packet.add_field(_Field(PacketFieldType.UNSIGNED_SHORT, int(port)))
        packet.add_field(_Field(PacketFieldType.VARINT, state))

        return packet.Build()

    @staticmethod
    def get_login_start(name: str, player_uuid: str = None, debug=False) -> bytes:
        import uuid

        if player_uuid is None:
            player_uuid = uuid.uuid3(
                uuid.NAMESPACE_DNS,
                "OfflinePlayer:" + name
            ).bytes

        packet = PacketBuilder(0x00, debug)

        packet.add_field(_Field(PacketFieldType.STRING, str(name)))
        packet.add_field(_Field(PacketFieldType.UUID, player_uuid))

        return packet.Build()

    @staticmethod
    def get_status_request(debug=False):
        packet = PacketBuilder(0x00, debug)
        return packet.Build()

    @staticmethod
    def get_login_acknowledged(debug=False,build=True):
        packet = PacketBuilder(0x03, debug)
        if build:
            return packet.Build()
        else:
            return packet

    @staticmethod
    def get_acknowledge_finish_configuration(debug=False,build=False):
        packet = PacketBuilder(0x03, debug)
        if build:
            return packet.Build()
        else:
            return packet

    @staticmethod
    def get_finish_config(debug=False):
        packet = PacketBuilder(0x02, debug)
        return packet.Build()

    @staticmethod
    def get_keepalive(keep_id, debug=False,build=False):
        packet = PacketBuilder(0x04, debug)
        packet.add_field(_Field(PacketFieldType.LONG, keep_id))
        if build:
            return packet.Build()
        else:
            return packet
