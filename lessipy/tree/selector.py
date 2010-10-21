import lessipy.tree.cssable


class Selector(lessipy.tree.cssable.CSSable):
    """A css selector."""

    def __init__(self, key):
        self.key = key

    def __gt__(self, selector):
        return Selector(self.key + " > " + selector.key)

    def __add__(self, selector):
        if isinstance(selector, ChildSelector):
            return self.__gt__(selector)
        return Selector(self.key + " " + selector.key)

    def to_css(self):
        return str(self.key)


class ChildSelector(Selector):
    """A child selector."""
