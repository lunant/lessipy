import lessipy.tree.node


class Expression(lessipy.tree.node.Node):

    __slots__ = "value", # List of expressions

    def __init__(self, expressions):
        self.value = expressions
