import lessipy.tree.node


class Mixin(lessipy.tree.node.Node):
    
    __slots__ = "value",

    def __init__(self, mixin):
        self.value = mixin
