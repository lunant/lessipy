import lessipy.tree.node


class Operand(lessipy.tree.node.Node):
    """An abstract class for all of calculatable(operable) numerics."""

    @property
    def result(self):
        """All operands must has a evaluated result."""
        return self

    def __numeric__(self):
        """All operands must implement `__numeric__()` function."""
        raise NotImplementedError("operand instance is not `Numeric`")

    def basic(self, other, __method__):
        """The basic operation method"""
        lval = self.result
        rval = other.result
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
