# read version from installed package
from importlib.metadata import version
__version__ = version('pycounts_gaurav')

from pycounts_gaurav.pycounts_gaurav import count_words
from pycounts_gaurav.plotting import plot_words