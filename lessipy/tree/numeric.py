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

    __slots__ = "value",

    def __init__(self, value):
        """Creates a number.
        
        :param val: a numeric value. (e.g 1, 1.0, 0x22)

        """
        try:
            self.value = int(value)
        except ValueError:
            self.value = float(value)
        self.unit = None

    @property
    def result(self):
        return self

    def __numeric__(self):
        """Returns numeric value"""
        return numeric(self.value)

    def unify(self, other):
        """Unifies `Numeric` or `Dimension` unit."""
        try:
            if not self.result.unit or not other.result.unit:
                return self.result.unit if self.result.unit else \
                           other.result.unit
            elif self.result.unit == other.result.unit:
                return self.result.unit
            raise ArithmeticError("It is impossible to operate "  \
                                 + repr(self.result.unit) + " and " + \
                                  repr(other.result.unit))
        except AttributeError:
            raise ArithmeticError("It is impossible to operate "  \
                                  + repr(self) + " and " + repr(other))

    def basic(self, other, __method__):
        """The basic operation method"""
        lval = self.result
        rval = other.result
        unit = self.unify(rval)
        result = getattr(float(numeric(lval)), __method__)(float(numeric(rval)))
        if unit:
            return Dimension(Numeric(result), unit)
        return self.__class__(Numeric(result), unit)
