import lessipy.tree.cssable


class Selector(lessipy.tree.cssable.CSSable):
    """A css selector."""

    def __init__(self, key):
        self.key = key

    def __gt__(self, selector):
        # self > selector

    def __add__(self, selector):
        # self selector

    def to_css(self):
        return str(self.key)

