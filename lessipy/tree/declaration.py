import lessipy.tree.node


class Declaration(lessipy.tree.node.Node):

    __slots__ = "name", "value"

    def __init__(self, declaration):
        self.name = declaration[0] # variable, property name
        self.value = declaration[1] # expression
