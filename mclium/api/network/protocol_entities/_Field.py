from mclium.mclium_types import PacketFieldType

class _Field:
    def __init__(
        self,
        field_type: PacketFieldType,
        value=None,
        optional: bool = False
    ):
        self.field_type = field_type
        self.value = value
        self.optional = optional
