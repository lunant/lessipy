import lessipy.tree.operator
import lessipy.tree.ruleset


__universal__ = lessipy.tree.ruleset.__universal__


class Variable(lessipy.tree.operator.Operand):
    """A LESS variable."""

    def __init__(self, key):
        self.key = key

    def evaluate(self, context=__universal__):
        try:
            return context.declarations[self.__class__][self.key]
        except KeyError:
            return self.evaluate(context.parent)
        except AttributeError:
            raise NameError("no such variable, " + repr(self))
