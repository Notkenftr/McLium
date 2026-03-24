import os
from mclium import Path
class InstalledLib:
    @staticmethod
    def _read_cache():
        cache_file = os.path.join(Path.getRootPath(), '.cache', 'installed.txt')

        if not os.path.exists(cache_file):
            return set()

        with open(cache_file) as f:
            return set(line.strip() for line in f if line.strip())
    @staticmethod
    def _write_cache(packages):
        cache_file = os.path.join(Path.getRootPath(), '.cache', 'installed.txt')

        with open(cache_file, 'a') as f:
            for pkg in packages:
                f.write(pkg + "\n")
