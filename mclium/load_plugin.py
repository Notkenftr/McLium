import os
import subprocess

import yaml
from mclium import Path
import sys
import importlib.util
from importlib.metadata import distributions

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

        self.require_libraries = self.data.get('require_libraries', [])

        self.depend = self.data.get('depend', [])
        self.softdepend = self.data.get('softdepend', [])


    def _read(self):
        with open(self.yml_path, "r") as f:
            return yaml.safe_load(f)


def _read_cache():
    cache_file = os.path.join(Path.getRootPath(), '.cache', 'installed.txt')

    if not os.path.exists(cache_file):
        return set()

    with open(cache_file) as f:
        return set(line.strip() for line in f if line.strip())

def _write_cache(packages):
    cache_file = os.path.join(Path.getRootPath(), '.cache', 'installed.txt')

    with open(cache_file, 'a') as f:
        for pkg in packages:
            f.write(pkg + "\n")

def load():
    global plugin_yml
    import types

    plugins = {}
    loaded = set()

    print("[PLuginLoader] Checking installed libs...")

    installed_libs = set()

    for folder in os.listdir(plugin_dir):
        pl_path = os.path.join(plugin_dir, folder)
        if not os.path.isdir(pl_path):
            continue

        yml_path = os.path.join(pl_path, "plugin.yml")
        if not os.path.exists(yml_path):
            continue

        plugin_yml = PluginYml(yml_path)
        plugins[plugin_yml.name] = (plugin_yml, pl_path)

    for name, (plugin_yml, _) in plugins.items():
        for lib in plugin_yml.require_libraries:
            if lib not in installed_libs:
                print(f"[PluginLoader] Installing lib: {lib}")

                subprocess.call([sys.executable, '-m', 'pip', 'install', lib,'-t',f'{os.path.join(Path.getRootPath(),'libraries')}'],
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL)

                installed_libs.add(lib)
                _write_cache(lib)

    changed = True

    while changed:
        changed = False

        for name, (plugin_yml, pl_path) in list(plugins.items()):

            package_name = name
            package = types.ModuleType(package_name)
            package.__path__ = [pl_path]
            sys.modules[package_name] = package

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
            print(f"[PluginLoader] Loaded {name} v{plugin_yml.version}")
    for name, (plugin_yml, _) in plugins.items():
        for d in plugin_yml.depend:
            if d not in loaded:
                raise Exception(f"Plugin {name} missing dependency {d}")

    return loaded
