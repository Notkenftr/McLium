import sys
import os

root = os.path.dirname(os.path.abspath(__file__))
libraries_dir = os.path.join(root, "libraries")

sys.path = [p for p in sys.path if "site-packages" not in p]

sys.path.insert(0, libraries_dir)

from mclium.initialization import Initialization

if __name__ == "__main__":
    Initialization()

    from mclium.main import init_parser
    init_parser()
