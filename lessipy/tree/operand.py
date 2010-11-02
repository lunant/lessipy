import lessipy.tree.node


class Operand(lessipy.tree.node.Node):
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


class Operator(Operand):
    """An operator class for variable operation."""

    def __init__(self, lval, rval):
        for el in (lval, rval):
            if not isinstance(el, Operand):
                raise ValueError("lval and rval should be `Operand` instance"
                                 ", passed" + repr(el))
        self.lval, self.rval = lval, rval


class Addition(Operator):
    """Do add."""

    def evaluate(self):
        return self.lval.evaluate() + self.rval.evaluate()


class Subtraction(Operator):
    """Do subtract."""

    def evaluate(self):
        return self.lval.evaluate() - self.rval.evaluate()


class Multiplication(Operator):
    """Do multiply."""

    def evaluate(self):
        return self.lval.evaluate() * self.rval.evaluate()

class Division(Operator):
    """Do devide."""

    def evaluate(self):
        return self.lval.evaluate() / self.rval.evaluate()
