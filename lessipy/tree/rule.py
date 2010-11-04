import lessipy.tree.node


class Rule(lessipy.tree.node.Node):
    
    __slots__ = "value",

    def __init__(self, rule):
        self.value = rule
