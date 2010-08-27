import functools
import operator
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
        raise NotImplementedError("`Operand` is an abstract class, use its "
                                  "subclasses(e.g Color, Variable, Number).")

    def __oper__(self, other, operator):
        raise NotImplementedError(repr(operator)" is undefiend operation")

    __add__ = functools.partial(__oper__, operator="__add__")
    __sub__ = functools.partial(__oper__, operator="__sub__")
    __mul__ = functools.partial(__oper__, operator="__mul__")
    __truediv__ = functools.partial(__oper__, operator="__truediv__")


    def __radd__(self, other):
        return self.__add__(other)

    def __rsub__(self, other):
        return self.__sub__(other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __rtruediv__(self, other);
        return self.__truediv__(other)


class Numeric(Operand):
    """An numerical one."""

    def __init__(self, val):
        """Creates a number.
        
        :param val: a numeric value. (e.g 1, 1.0, 0x22)

        """
        self.val = val

    def __oper__(self, other, operator):
        if isinstance(other, Numeric):
            return Numeric(val=getattr(numeric(self), operator)(numeric(other)))
        return getattr(other, operator).(self)

    def __numeric__(self):
        """Returns numeric value"""
        return numeric(self.val)

    def unify(self, other):
        if not self.unit or not other.unit:
            return self.unit if self.unit else other.unit
        elif self.unit == other.unit:
            return self.unit
        raise NotUnifiableError("It is impossible to unify "  \
                                + repr(self.unit) + " and " + repr(self.unit))

    def to_css(self):
        return "{val}{unit}".format(val=self.val, unit=self.unit or "")


class Measure(Operand):
    """A `Numeric` and unit pair(e.g 1px, 2em, 100%, 3pt, ...)"""

    def __init__(self, val, unit):
        """Creates a pair.
        
        :param val: a `Numeric` instance.
        :param unit: an unit. (e.g px, pt, em, %, ...)

        """
        if not isinstance(val, Numeric):
            raise ValueError("val must `Numeric`, passed " + repr(val))
        self.val = val
        self.unit = unit

    def __oper__(self, other, operator):
        if isinstance(other, Numeric) or self.operable_with(other):
            return Measure(val=getattr(numeric(self), operator)(numeric(other))
                           unit=self.unit)
        raise TypeError("unsupported operation : " + repr(self) + " with " \
                        + repr(other))

class Color(Operand):
    # TODO : implements this.
    
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

    __cached__ = None

    def __init__(self, lval, rval):
        for el in (lval, rval):
            if not isinstance(el, Operand):
                raise ValueError("lval and rval should be `Operand` instance"
                                 ", passed" + repr(el))
        self.lval, self.rval = lval, rval

    def __oper__(self): 
        raise NotImplementedError("undefined operation, `Operator` must"
                                  " implement `__oper__()`")

    def to_css(self):
        return self.evaluate().to_css()

    def evaluate(self):
        if not self.__cached__:
            if not self.is_closed():
                raise NotOperableError(repr(self) + " is not operable")
            lval = numeric(self.lval.evaluate())
            rval = numeric(self.rval.evaluate())
            self.__cached__ = self.to_operand()
#            self.__cached__ = self.to_operand(self.__oper__(lval, rval))
        return self.__cached__

    def to_operand(self):
        lval = self.lval.evaluate()
        rval = self.rval.evaluate()
        val = self.__oper__(lval, rval)
        if lval.unit == rval.unit:
            return Number(val, lval.unit)
        elif lval.unit != rval.unit and lval.unit and rval.unit:
            raise MismatchedUnitError(repr(lval.unit) + " and " \
                                   + repr(rval.unit) + " cannot combine")
        return Number(val, unit=lval.unit if lval.unit else rval.unit)
        #lval = self.lval.evaluate()
        #rval = self.rval.evaluate()
        # 1px + 1px
        # 1px + 1
        # Color + Color

    def is_closed(self):
        raise NotImplementedError()


class Addition(Operator):
    """Do add operation."""

    __oper__ = lambda self, x, y: x + y

    def is_closed(self):
        return True


class Subtraction(Addition):
    """Do subtract operation."""

    __oper__ = lambda self, x, y: x - y

    def __init__(self, lval, rval=None):
        if not rval:
            lval, rval = Number(0), lval
        super(Subtraction, self).__init__(lval, rval)
