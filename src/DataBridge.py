class DataBridge:
    _subparser = None

    @classmethod
    def set_subparser(cls, subparser):
        cls._subparser = subparser

    @classmethod
    def get_subparser(cls):
        if cls._subparser is None:
            raise RuntimeError("Subparser has not been initialized")
        return cls._subparser
