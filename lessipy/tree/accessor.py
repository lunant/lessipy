import lessipy.tree.node


class Accessor(lessipy.tree.node.Node):

    __slots__ = "name", "value",

    def __init__(self, accessor):
        self.name = accessor[0] # selector
        self.value = accessor[1] # identifier(property, variable)
