import numbers
from lessipy.tree.numeric import Numeric


class Dimension(Numeric):
    """A `Numeric` and unit pair(e.g 1px, 2em, 100%, 3pt, ...)"""

    def __init__(self, args):
        """Creates a pair.
        
        :param val: a `Numeric` instance or `int`.
        :param unit: an unit. (e.g px, pt, em, %, ...)

        """
        val = args[0]
        unit = args[1]
        if isinstance(val, numbers.Number):
            val = Numeric(val)
        if unit == '%':
            self.val = val.val / 100.0
            self.unit = None
        else:
            self.val = val
            self.unit = unit

