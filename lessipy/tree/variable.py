import lessipy.tree.node


class Variable(lessipy.tree.node.Node):
    
    __slots__ = "value",

    def __init__(self, variable):
        self.value = variable
