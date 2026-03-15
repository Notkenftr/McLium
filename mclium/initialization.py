import re
import os
import sys
import subprocess
from mclium import Path
from importlib.metadata import distributions


class Initialization:
    def __init__(self):
        self._create_folder()
        self.package_list = self._read_requirements()
        self.cached_packages = self._read_cache()
        self.install_list = self._check_libraries()

    def _create_folder(self):
        root = Path.getRootPath()
        os.makedirs(os.path.join(root,"libraries"), exist_ok=True)
        os.makedirs(os.path.join(root, "mc4j"), exist_ok=True)
        os.makedirs(os.path.join(root,"mc4j","docker"),exist_ok=True)
        os.makedirs(os.path.join(root, 'data'), exist_ok=True)
        os.makedirs(os.path.join(root, 'logs'), exist_ok=True)
        os.makedirs(os.path.join(root, '.cache'), exist_ok=True)

    def _read_requirements(self):
        path = os.path.join(Path.getRootPath(), 'data', 'requirements.txt')
        names = []

        with open(path) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                name = re.split(r'[<>=!~]', line)[0].strip().lower()
                names.append(name)

        return names

    def _read_cache(self):
        cache_file = os.path.join(Path.getRootPath(), '.cache', 'installed.txt')

        if not os.path.exists(cache_file):
            return set()

        with open(cache_file) as f:
            return set(line.strip() for line in f if line.strip())

    def _write_cache(self, packages):
        cache_file = os.path.join(Path.getRootPath(), '.cache', 'installed.txt')

        with open(cache_file, 'a') as f:
            for pkg in packages:
                f.write(pkg + "\n")

    def _check_libraries(self):
        installed = {
            dist.metadata["Name"].lower()
            for dist in distributions()
        }

        install = []

        for pkg in self.package_list:

            if pkg in self.cached_packages and pkg in installed:
                continue

            if pkg not in installed:
                print(f"Installing missing package: {pkg}")
                subprocess.check_call(
                    [
                        sys.executable,
                        "-m",
                        "pip",
                        "install",
                        pkg,
                        "--target",
                        os.path.join(Path.getRootPath(), "libraries")
                    ]
                )
                install.append(pkg)

        if install:
            self._write_cache(install)

        return install
