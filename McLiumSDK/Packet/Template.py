from enum import Enum
from McLiumSDK import PacketBuilder
from McLiumSDK import FieldType

class ReadyForUsingPck:
    @staticmethod
    def HandshakeState1(protocol,
                        address,
                        port) -> PacketBuilder:
        packet = PacketBuilder(0x00)
        packet.add_field(PacketBuilder.Field(FieldType.VARINT,int(protocol)))
        packet.add_field(PacketBuilder.Field(FieldType.STRING,str(address)))
        packet.add_field(PacketBuilder.Field(FieldType.INT,int(port)))
        packet.add_field(PacketBuilder.Field(FieldType.VARINT,1))
        return packet.Build()

    @staticmethod
    def HandshakeState2(protocol,
                        address,
                        port) -> PacketBuilder:
        packet = PacketBuilder(0x00)
        packet.add_field(PacketBuilder.Field(FieldType.VARINT, int(protocol)))
        packet.add_field(PacketBuilder.Field(FieldType.STRING, str(address)))
        packet.add_field(PacketBuilder.Field(FieldType.INT, int(port)))
        packet.add_field(PacketBuilder.Field(FieldType.VARINT, 2))
        return packet.Build()

    @staticmethod
    def HandshakeState3(protocol,
                        address,
                        port) -> PacketBuilder:
        packet = PacketBuilder(0x00)
        packet.add_field(PacketBuilder.Field(FieldType.VARINT, int(protocol)))
        packet.add_field(PacketBuilder.Field(FieldType.STRING, str(address)))
        packet.add_field(PacketBuilder.Field(FieldType.INT, int(port)))
        packet.add_field(PacketBuilder.Field(FieldType.VARINT, 3))
        return packet.Build()