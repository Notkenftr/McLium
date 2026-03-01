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

        self.main = self.data.get('main')
        self.name = self.data.get('name')
        self.description = self.data.get('description', "")
        self.version = str(self.data.get('version', "1.0"))
        self.author = self.data.get('author', [])

        self.depend = self.data.get('depend', [])
        self.softdepend = self.data.get('softdepend', [])

    def _read(self):
        with open(self.yml_path, "r") as f:
            return yaml.safe_load(f)



def load():

    plugins = {}
    loaded = set()

    for folder in os.listdir(plugin_dir):
        pl_path = os.path.join(plugin_dir, folder)
        if not os.path.isdir(pl_path):
            continue

        yml_path = os.path.join(pl_path, "plugin.yml")
        if not os.path.exists(yml_path):
            continue

        plugin_yml = PluginYml(yml_path)
        plugins[plugin_yml.name] = (plugin_yml, pl_path)

    changed = True

    while changed:
        changed = False

        for name, (plugin_yml, pl_path) in list(plugins.items()):

            if name in loaded:
                continue

            missing = [d for d in plugin_yml.depend if d not in loaded]
            if missing:
                continue

            waiting_soft = [
                s for s in plugin_yml.softdepend
                if s in plugins and s not in loaded
            ]
            if waiting_soft:
                continue

            entry = plugin_yml.main
            module_name, class_name = entry.rsplit('.', 1)
            module_path = os.path.join(pl_path, module_name + ".py")

            spec = importlib.util.spec_from_file_location(
                f"{name}.{module_name}",
                module_path
            )

            module = importlib.util.module_from_spec(spec)
            sys.modules[f"{name}.{module_name}"] = module
            spec.loader.exec_module(module)

            clazz = getattr(module, class_name)
            instance = clazz()
            instance.register_subcommand()

            loaded.add(name)
            changed = True

    for name, (plugin_yml, _) in plugins.items():
        for d in plugin_yml.depend:
            if d not in loaded:
                raise Exception(f"Plugin {name} missing dependency {d}")

    return loaded
