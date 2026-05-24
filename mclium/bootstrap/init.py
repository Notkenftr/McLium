from mclium.manager.plugin_manager import PluginManager
from mclium.context.memory_context import MemoryContext
from mclium.loader import Loader
from mclium.term_ui.term_ui import TermUi

def start_init():
    PluginManager().init()
    MemoryContext().init()
    Loader().init()


    print(PluginManager().get_plugins())
if __name__ == '__main__':
    start_init()
    TermUi().run()
