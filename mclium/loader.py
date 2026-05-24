import json
import os
import yaml
import inspect
import importlib
from mclium.utils import Path
from mclium.manager.plugin_manager import PluginManager
class Loader:
    def __init__(self):
        self.plugins_path = Path.join_path("plugins")
        self.plugins = [
            p for p in os.listdir(self.plugins_path)
            if os.path.isdir(os.path.join(self.plugins_path, p))
        ]

    def depend_handler(self,depends):
        pass

    def load_plugin(self,pl):
        plugin_path = os.path.join(self.plugins_path, pl)
        if not os.path.exists(plugin_path):
            return None
        if os.path.exists(os.path.join(self.plugins_path, pl,"plugin.yml")):
            with open(
                os.path.join(plugin_path, "plugin.yml"), 'r', encoding="utf-8"
            ) as f:
                plugin_info = yaml.safe_load(f)

        elif os.path.exists(os.path.join(self.plugins_path, pl,"plugin.yaml")):
            with open(
                os.path.join(plugin_path, "plugin.yaml"), 'r', encoding="utf-8"
            ) as f:
                plugin_info = yaml.safe_load(f)

        elif os.path.exists(os.path.join(self.plugins_path, pl,"plugin.json")):
            with open(
                os.path.join(plugin_path, "plugin.json"), 'r', encoding="utf-8"
            ) as f:
                plugin_info = json.load(f)
        else:
            return None

        main = plugin_info.get("main",None)

        #get module name and main_class | main.app -> main app
        module_name,main_class = main.split(".")

        # import | plugins.main.app
        import_path = f"plugins.{pl}.{module_name}"

        module = importlib.import_module(import_path)

        if hasattr(module,main_class):
            plugin_class = getattr(module,main_class,None)
            if plugin_class is not None and inspect.isclass(plugin_class):
                plugin_instance = plugin_class()
                return plugin_instance

        return None

    def load_all_plugins(self):
        plugins_instance = []
        for pl in self.plugins:
            plugin_instance = self.load_plugin(pl)
            if plugin_instance is not None:
                plugins_instance.append(plugin_instance)

        return plugins_instance

    def init(self):
        plugins_instance = self.load_all_plugins()
        PluginManager().add_plugins(plugins_instance)


if __name__ == '__main__':
    from mclium.manager.plugin_manager import PluginManager
    from mclium.context.memory_context import MemoryContext

    PluginManager().init()
    MemoryContext().init()

    loader = Loader()
    loader.init()

    print(PluginManager().get_plugins())
