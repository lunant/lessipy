import lessipy.tree.node


class Comment(lessipy.tree.node.Node):
    
    __slots__ = "value",
    
    def __init__(self, comment):
        self.value = comment

