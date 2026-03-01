import os
import yaml
from mclium import Path
import sys
import importlib.util
plugin_dir = Path.getPluginsPath()


class PluginYml:
    def __init__(self, yml_path):
        self.yml_path = yml_path
        self.data = self._read()

        self.main = self.data['main']
        self.name = self.data['name']
        self.description = self.data['description']
        self.version = str(self.data['version'])
        self.author = list(self.data['author'])

        self.depend = list(self.data['depend'])
        self.softdepend = list(self.data['softdepend'])

    def _read(self):
        with open(self.yml_path, "r") as f:
            return yaml.safe_load(f)




def load():
    for plugin in os.listdir(plugin_dir):
        pl = os.path.join(plugin_dir, plugin)
        if not os.path.isdir(pl):
            continue

        yml_path = os.path.join(pl, "plugin.yml")
        if not os.path.exists(yml_path):
            continue
        plugin_yml = PluginYml(yml_path)

        entry = plugin_yml.main
        module_name,class_name = entry.split('.',1)
        module_path = os.path.join(pl, module_name + ".py")

        spec = importlib.util.spec_from_file_location(
            module_name,
            module_path
        )

        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)

        clazz = getattr(module, class_name)

        instance = clazz()
        instance.register_subcommand()


