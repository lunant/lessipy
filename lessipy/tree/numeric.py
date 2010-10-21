import numbers
from lessipy.tree.operator import Operand


def numeric(cls):
    """Gets numeric value of a given object."""
    try:
        return cls.__numeric__()
    except AttributeError:
        if isinstance(cls, numbers.Number):
            return cls
    raise ValueError("cls must be numeric, passed " + repr(cls))


class Numeric(Operand):
    """A numerical."""

    def __init__(self, val):
        """Creates a number.
        
        :param val: a numeric value. (e.g 1, 1.0, 0x22)

        """
        try:
            self.val = int(val)
        except ValueError:
            self.val = float(val)
        self.unit = None

    def __numeric__(self):
        """Returns numeric value"""
        return numeric(self.val)

    def to_css(self):
        return str(self.val)

    def unify(self, other):
        """Unifies `Numeric` or `Measure` unit."""
        try:
            if not self.unit or not other.unit:
                return self.unit if self.unit else other.unit
            elif self.unit == other.unit:
                return self.unit
            raise ArithmeticError("It is impossible to operate "  \
                                 + repr(self.unit) + " and " + repr(other.unit))
        except AttributeError:
            raise ArithmeticError("It is impossible to operate "  \
                                  + repr(self) + " and " + repr(other))

    def basic(self, other, __method__):
        """The basic operation method"""
        lval = self.evaluate()
        rval = other.evaluate()
        unit = self.unify(rval)
        result = getattr(float(numeric(lval)), __method__)(float(numeric(rval)))
        if unit:
            return Measure(Numeric(result), unit)
        return self.__class__(Numeric(result), unit)


class Measure(Numeric):
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

    def to_css(self):
        return "{val}{unit}".format(val=self.val.to_css(), unit=self.unit)
