import doctest
from lessipy import *

doctest.testfile("tests/declaration.txt", optionflags=doctest.REPORT_ONLY_FIRST_FAILURE)
#doctest.testfile("tests/types.txt", raise_on_error=True)

