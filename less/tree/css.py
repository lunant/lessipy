import less.tree.cssable


class CSS(less.tree.cssable.CSSable):

    def __init__(self, name):
        """Make a new css instance.
        
        :param name: a standard css pre-defined keywords.


        """
        if name.__class__ != str:
            raise ValueError("`Property` or `Keyword` name must be str,"
                             "passed " + repr(name))
        self.name = name

    def to_css(self):
        return self.name
