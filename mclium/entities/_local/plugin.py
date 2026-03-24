import yaml

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
