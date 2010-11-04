import lessipy.tree.node


class Property(lessipy.tree.node.Node): 

    __slots__ = "value",

    def __init__(self, _property):
        self.value = _property
