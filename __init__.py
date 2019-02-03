import sys
from os.path import dirname, join

sys.path.append(join(dirname(__file__), 'lib'))

from . import main


main.load()
