import lessipy.tree.css
import lessipy.tree.operator
import lessipy.tree.ruleset
import lessipy.tree.declaration as declaration


__universal__ = lessipy.tree.ruleset.__universal__


class Property(lessipy.tree.css.CSS, lessipy.tree.operator.Operand):
    """A css standard property."""

    def evaluate(self, context=__universal__):
        try:
            return context.declarations[self.__class__][self.key]
        except KeyError:
            return self.evaluate(context.parent)
        except AttributeError:
            raise NameError("no such property, " + repr(self))

    def to_css(self, context=__universal__):
        try:
            return context.declarations[declaration.PropertyDeclaration][self.key]
        except KeyError:
            return self.to_css(context.parent)
        except AttributeError:
            raise NameError("No such property, " + repr(self))
