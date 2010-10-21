import lessipy.tree.node


class Expression(lessipy.tree.node.Node):
    """A css value expression. It just chaning elements."""

    def __init__(self, *elements):
        self.elements = elements

