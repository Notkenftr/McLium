import os
import sys
import types
import subprocess
from mclium import Path
from mclium.entities._local.plugin import PluginYml
from mclium.local_api.cache import InstalledLib

class Loader:
    def __init__(self):
        pass

    def start_load(self):
        plugins = {}
        loaded = set()

        print(f"[PluginLoader] Checking libs and downloads...")

        installed_libs = InstalledLib._read_cache()

        for folder in os.listdir(Path.getPluginsPath()):
            pl_path = os.path.join(Path.getPluginsPath(), folder)
            if not os.path.isdir(pl_path):
                continue

            yml_path = os.path.join(pl_path, "plugin.yml")
            if not os.path.exists(yml_path):
                continue

            plugin_yml: PluginYml = PluginYml(yml_path)
            plugins[plugin_yml.name] = plugin_yml


        for name, (plugin_yml, _) in plugins.items():
            for lib in plugin_yml.require_libraries:
                if lib not in installed_libs:
                    print(f"[PluginLoader] Installing {lib}")

                    subprocess.call([sys.executable, '-m', 'pip', 'install', lib, '-t',
                                     f'{os.path.join(Path.getRootPath(), 'libraries')}'],
                                    stdout=subprocess.DEVNULL,
                                    stderr=subprocess.DEVNULL)

                    installed_libs.add(lib)
                    InstalledLib._write_cache(lib)

        changed = True

        while changed:
            changed = False
            for name, (plugin_yml, _) in plugins.items():
                package_name = name
                package = types.ModuleType(package_name)
                package.__path__ = [pl_path] # set path của pl ở ./plugins/pl

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

                
