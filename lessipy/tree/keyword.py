import lessipy.tree.node


class Keyword(lessipy.tree.node.Node):

    __slots__ = "value",

    def __init__(self, keyword):
        self.value = keyword
