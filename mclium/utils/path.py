import os

root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir,os.pardir))

class Path:
    @staticmethod
    def get_root_path():
        return root

    @staticmethod
    def join_path(*args):
        return os.path.join(root,*args)


