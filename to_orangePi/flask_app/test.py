import numpy
import warnings

warnings.filterwarnings('error')

try:
    numpy.arccos(-2)
except Warning:
    print('sosi')