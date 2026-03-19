from enum import Enum

class BuildHookAt(Enum):

    BEFORE_BUILD = "BeforeBuild"

    BEFORE_FIELD_ADD = "BeforeFieldAdd"
    AFTER_FIELD_ADD = "AfterFieldAdd"

    BEFORE_LENGTH_ENCODE = "BeforeLengthEncode"
    AFTER_LENGTH_ENCODE = "AfterLengthEncode"

    AFTER_BUILD = "AfterBuild"
