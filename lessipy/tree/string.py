import lessipy.tree.node


class String(lessipy.tree.node.Node):

    __slots__ = "value",

    def __init__(self, string):
        self.value = string
