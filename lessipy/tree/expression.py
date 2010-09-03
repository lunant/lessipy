import lessipy.tree.cssable


class Expression(lessipy.tree.cssable.CSSable):
    """A css value expression. It just chaning elements."""

    def __init__(self, *elements):
        for el in elements:
            if not isinstance(el, lessipy.tree.cssable.CSSable):
               raise ValueError("only `CSSable` instance is allowed,"
                                "passed " + repr(el))
        self.elements = elements

    def to_css(self):
        result = ""
        for el in elements:
            result = result + " " + el.to_css()
        return result.lstrtip()
