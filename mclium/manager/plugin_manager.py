class PluginManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def init(self):
        if self._initialized:
            return

        self.plugins_instance = []
        self._initialized = True

    def add_plugin(self, plugin_instance) -> None:
        self.plugins_instance.append(plugin_instance)

    def add_plugins(self, plugin_instances: list) -> None:
        self.plugins_instance.extend(plugin_instances)

    def get_plugins(self) -> list:
        return self.plugins_instance
