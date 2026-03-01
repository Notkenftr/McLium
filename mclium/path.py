import os

root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

class Path:
    @staticmethod
    def getRootPath():
        return root
    @staticmethod
    def getPluginsPath():
        return os.path.join(root, 'plugins')
    @staticmethod
    def getConfigPath():
        return os.path.join(root, 'config')
    @staticmethod
    def getDataPath():
        return os.path.join(root, 'data')
    @staticmethod
    def getLogPath():
        return os.path.join(root, 'log')
