import doctest
from lessipy import *

doctest.testfile("tests/lessipy.txt", optionflags=doctest.REPORT_ONLY_FIRST_FAILURE)
