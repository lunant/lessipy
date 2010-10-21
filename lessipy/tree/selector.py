

class Selector(lessipy.tree.node.Node):
    """A css selector."""

    def __init__(self, key):
        self.key = key

    def __gt__(self, selector):
        return Selector(self.key + " > " + selector.key)

    def __add__(self, selector):
        if isinstance(selector, ChildSelector):
            return self.__gt__(selector)
        return Selector(self.key + " " + selector.key)


class ChildSelector(Selector):
    """A child selector."""
