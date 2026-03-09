import platform
from mclium.mclium_types import OsName
def os_detect():
    os_name = platform.system()
    for name in OsName:
        if name.value == os_name:
            return name
        else:
            return OsName.UNKNOWN
