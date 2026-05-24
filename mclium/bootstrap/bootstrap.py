from mclium.manager.plugin_manager import PluginManager
from mclium.context.memory_context import MemoryContext
from mclium.loader import Loader
from mclium.term_ui.term_ui import TermUi

import traceback

def bootstrap() -> None:
    try:
        PluginManager().init()
        MemoryContext().init()
        Loader().init()
        TermUi().run()
    except Exception as e:
        traceback.print_exc()
        raise RuntimeError(str(e))
