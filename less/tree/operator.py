import numbers
import less.tree.cssable


def numeric(cls):
    """Gets numeric value of a given object."""
    try:
        return cls.__numeric__()
    except AttributeError:
        if isinstance(cls, numbers.Number):
            return cls
    raise ValueError("cls must be numeric, passed " + repr(cls))


class Operand(less.tree.cssable.CSSable):
    """An abstract class for all of calculatable(operable) numerics."""

    def evaluate(self):
        """All operands must be evaluatable."""
        return self

    def __numeric__(self):
        """All operands must implement `__numeric__()` function."""
        raise NotImplementedError("operand instance is not `Numeric`")

    def basic(self, other, __method__):
        """The basic operation method"""
        lval = self.evaluate()
        rval = other.evaluate()
        return self.__class__(getattr(numeric(lval), __method__)(numeric(rval)))

    for __method__ in "__add__", "__sub__", "__mul__", "__truediv__":
        def __operator__(self, other, __method__=__method__):
            return self.basic(other, __method__)
        locals()[__method__] = __operator__
        del __operator__
    del __method__

    def __radd__(self, other):
        return self.__add__(other)

    def __rsub__(self, other):
        return self.__sub__(other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __rtruediv__(self, other):
        return self.__truediv__(other)


class Numeric(Operand):
    """An numerical one."""

    def __init__(self, val):
        """Creates a number.
        
        :param val: a numeric value. (e.g 1, 1.0, 0x22)

        """
        self.val = val
        self.unit = None

    def __numeric__(self):
        """Returns numeric value"""
        return numeric(self.val)

    def to_css(self):
        return str(self.val)

    def basic(self, other, __method__):
        """The basic operation method"""
        lval = self.evaluate()
        rval = other.evaluate()
        unit = self.unify(rval)
        result = getattr(numeric(lval), __method__)(numeric(rval))
        if unit:
            return Measure(Numeric(result), unit)
        return self.__class__(Numeric(result), unit)

    def unify(self, other):
        if not self.unit or not other.unit:
            return self.unit if self.unit else other.unit
        elif self.unit == other.unit:
            return self.unit
        raise ArithmeticError("It is impossible to operate "  \
                              + repr(self.unit) + " and " + repr(other.unit))


class Measure(Numeric):
    """A `Numeric` and unit pair(e.g 1px, 2em, 100%, 3pt, ...)"""

    def __init__(self, val, unit):
        """Creates a pair.
        
        :param val: a `Numeric` instance or `int`.
        :param unit: an unit. (e.g px, pt, em, %, ...)

        """
        if isinstance(val, numbers.Number):
            val = Numeric(val)
        if not isinstance(val, Numeric):
            raise ValueError("val must `Numeric`, passed " + repr(val))
        self.val = val
        self.unit = unit

    def to_css(self):
        return str(self.val.to_css()) + str(self.unit)


class Color(Operand):
    """A set of red, green, blue colorset."""
    
    def __init__(self, r, g, b):
        pass


class HexColor(Operand):

    @classmethod
    def from_digit(cls, digit):
        rgba = []
        for x in xrange(4, 0, -1):
            channel = digit % (255 ** x)
            digit = digit / (255 ** x)
            rgba.append(channel)
        return [min(channel, 255) for channel in rgba]


class Operator(Operand):
    """An operator class for variable operation."""

    def __init__(self, lval, rval):
        for el in (lval, rval):
            if not isinstance(el, Operand):
                raise ValueError("lval and rval should be `Operand` instance"
                                 ", passed" + repr(el))
        self.lval, self.rval = lval, rval

    def to_css(self):
        return self.evaluate().to_css()


class Addition(Operator):
    """Do add."""

    def evaluate(self):
        return self.lval.evaluate() + self.rval.evaluate()


class Subtraction(Operator):
    """Do subtract."""

    def evaluate(self):
        return self.lval.evaluate() - self.rval.evaluate()


class Multiply(Operator):
    """Do multiply."""

    def evaluate(self):
        return self.lval.evaluate() * self.rval.evaluate()

class Division(Operator):
    """Do devide."""

    def evaluate(self):
        return self.lval.evaluate() / self.rval.evaluate()
