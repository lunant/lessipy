import operator
import less.tree.cssable


class Operand(less.tree.cssable.CSSable):

    def evaluate(self):
        return self

    def __float__(self):
        raise NotImplementedError()


class Number(Operand):

    def __init__(self, val, unit=None):
        self.val, self.unit = float(val), unit

    def __float__(self):
        return self.val

    def to_css(self):
        val = int(self.val) if round(self.val) == self.val else self.val
        return "{val}{unit}".format(val=val, unit=self.unit or "")


class Color(Operand):
    
    def __init__(self, r, g, b, a=255):
        pass

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

    def to_css(self):
        return self.evaluate().to_css()

    def evaluate(self):
        if not self.__cached__:
            if not self.is_closed():
                raise NotOperatableError("impossible operation")
            lval = float(self.lval.evaluate())
            rval = float(self.rval.evaluate())
            self.__cached__ = self.make_operand(self.__oper__(lval, rval))
        return self.__cached__

    def make_operand(self, val):
        lval = self.lval.evaluate()
        rval = self.rval.evaluate()
        if lval.unit == rval.unit:
            return Number(val, lval.unit)
        elif lval.unit != rval.unit and lval.unit and rval.unit:
            raise NotOperatableError(repr(lval.unit) + " and " \
                                   + repr(rval.unit) + " operation is "
                                     "impossible")
        return Number()
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
