import lessipy.tree.node


class Selector(lessipy.tree.node.Node):
    
    __slots__ = "value",

    def __init__(self, selector):
        self.value = selector 
