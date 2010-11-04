import lessipy.tree.node

class Import(lessipy.tree.node.Node):
    
    __slots__ = "value"

    def __init__(self, file):
        self.value = file  
