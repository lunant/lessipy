import numbers
from lessipy.tree.operand import Operand


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

    def unify(self, other):
        """Unifies `Numeric` or `Dimension` unit."""
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
            return Dimension(Numeric(result), unit)
        return self.__class__(Numeric(result), unit)
