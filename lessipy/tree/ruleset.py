import lessipy.tree.node


class Ruleset(lessipy.tree.node.Node):
    
    __slots__ = "value",

    def __init__(self, ruleset):
        self.name = ruleset[0] # selector 
        self.value = ruleset[1] # rules
        print repr(ruleset)
