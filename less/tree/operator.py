import PIL.ImageColor
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

def to_hexcode(cls):
    """Gets a hexcode from a `Color` instance."""
    if not isinstance(cls, Color):
        raise ValueError("only `Color` instance is convertable, passed" \
                         + repr(cls))
    return "#%02X%02X%02X" % (cls.red, cls.green, cls.blue)


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
    """A numerical."""

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
        return "{val}{unit}".format(val=self.val.to_css(), unit=self.unit)


class Color(Operand):
    
    def __new__(cls, colorset):
        if cls is not Color:
            return object.__new__(cls)
        if isinstance(colorset, str):
            return HexColor(colorset)
        if len(colorset) == 3:
            return RGBColor(colorset)
        if len(colorset) == 4:
            return RGBAColor(colorset)
        raise ValueError("only (r,g,b), (r,g,b,a) and '#hexcode' string are "
                         "allowed. passed " + repr(args))

    def basic(self, other, __method__):
        rgb = ("red", "green", "blue")
        colorset = []
        if other.__class__ is Numeric:
            for k in range(0, 3):
                colorset.insert(k, int(numeric(other)))
            other = RGBColor(colorset)
            colorset = []
        if not isinstance(other, Color):
            raise ArithmeticError("`Color` instance is able to operate with `"
                                  "`Color`, `Numeric`")
        for k in range(0, 3):
            colorset.insert(k, getattr(getattr(self, rgb[k]) * self.alpha, 
                                        __method__
                               )(getattr(other, rgb[k]) * other.alpha))
        return RGBColor(colorset)


class RGBColor(Color):
    """A set of red, green, blue, alpha colorset. Alpha is always 1.0."""

    alpha = 1.0

    def __init__(self, colorset):
        """Creates a color from rgb colorset.
        
        :param args: a digit number(0-255) set.
        
        """
        for color in colorset:
            if not isinstance(color, int):
                raise ValueError("colorset must be an `int` instance, passed " \
                                 + repr(color))
            if not(0 <= color <= 255):
                raise ValueError("colorset elements must be in valid range(0 "
                                 "to 255), passed " + repr(color))
        self.red = colorset[0]
        self.green = colorset[1]
        self.blue = colorset[2]

    def to_hex(self):
        return HexColor(to_hexcode(self))

    def to_css(self):
        return "rgb({r}, {g}, {b})".format(r=self.red, g=self.green,
                                           b=self.blue)


class RGBAColor(RGBColor):
    """A set of red, green, blue, alpha colorset."""

    def __init__(self, colorset):
        """Creates a color from rgba colorset.

        :param args: three digit numbers(0-255) and one float number(0-1).

        """
        super(RGBAColor, self).__init(self, *colorset)
        if not isinstance(colorset[3], float):
            raise ValueError("an alpha must be a `float` instance, passed " \
                             + repr(colorset[3]))
        if not(0 <= colorset[3] <= 1):
            raise ValueError("an alpha must be in valid range(0 to 1.0), " 
                             "passed " + repr(colorset[3]))
        self.alpha = colorset[3]

    def to_css(self):
        return "rgb({r}, {g}, {b}, {a})".format(r=self.red, g=self.green,
                                                b=self.blue, a=self.alpha)
    
    def to_rgb(self):
        return RGBColor((self.red * self.alpha, self.green * self.alpha,
                         self.blue * self.alpha))

    def to_hex(self):
        return self.to_rgb().to_hex()
        


class HexColor(Color):
    """A hexadecimal color code."""

    alpha = 1.0

    def __init__(self, hexcode):
        rgb = PIL.ImageColor.getrgb(hexcode)
        self.hexcode = hexcode
        self.red = rgb[0]
        self.green = rgb[1]
        self.blue = rgb[2]

    def to_css(self):
        return to_hexcode(self)

    def to_rgb(self):
        return RGBColor(self.red, self.green, self.blue)


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
