import os

root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
class PathManager:
    @staticmethod
    def getRoot():
        return root