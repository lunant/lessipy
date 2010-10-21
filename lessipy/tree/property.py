import lessipy.tree.operator
import lessipy.tree.ruleset


class Property(lessipy.tree.operator.Operand):
    """A css standard property."""

    def evaluate(self, context):
        try:
            return context.declarations[self.__class__][self.key]
        except KeyError:
            return self.evaluate(context.parent)
        except AttributeError:
            raise NameError("no such property, " + repr(self))

