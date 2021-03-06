import PIL.ImageColor
from lessipy.tree.operand import Operand
from lessipy.tree.numeric import *


def to_hexcode(cls):
    """Gets a hexcode from a `Color` instance."""
    if not isinstance(cls, Color):
        raise ValueError("only `Color` instance is convertable, passed" \
                         + repr(cls))
    return "#%02X%02X%02X" % (cls.red, cls.green, cls.blue)


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
                colorset.insert(k, int(getattr(
                    getattr(self, rgb[k]) * self.alpha, __method__)(other.val)
                ))
            return RGBColor(colorset)
        if not isinstance(other, Color):
            raise ArithmeticError("`Color` instance is able to operate with `"
                                  "`Color`, `Numeric`")
        for k in range(0, 3):
            colorset.insert(k, int(getattr(getattr(self, rgb[k]) * self.alpha, 
                                        __method__
                               )(getattr(other, rgb[k]) * other.alpha)))
        return RGBColor(colorset)


class RGBColor(Color):
    """A set of red, green, blue, alpha colorset. Alpha is always 1.0."""

    alpha = 1.0

    def __init__(self, colorset):
        """Creates a color from rgb colorset.
        
        :param args: a digit number(0-255) set.
        
        """
        for color in range(0, 2):
            if not(0 <= int(colorset[color]) <= 255):
                raise ValueError("colorset elements must be in valid range(0 "
                                 "to 255), passed " + repr(color))
        self.red = int(colorset[0])
        self.green = int(colorset[1])
        self.blue = int(colorset[2])

    def to_hex(self):
        return HexColor(to_hexcode(self))


class RGBAColor(RGBColor):
    """A set of red, green, blue, alpha colorset."""

    def __init__(self, colorset):
        """Creates a color from rgba colorset.

        :param args: three digit numbers(0-255) and one float number(0-1).

        """
        super(RGBAColor, self).__init__(colorset)
        if not(0 <= float(colorset[3]) <= 1):
            raise ValueError("an alpha must be in valid range(0 to 1.0), " 
                             "passed " + repr(int(colorset[3])))
        self.alpha = float(colorset[3])

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

    def to_rgb(self):
        return RGBColor(self.red, self.green, self.blue)
