import collections
import lessipy.tree.ruleset


BaseDeclaration = collections.namedtuple("BaseDecl", "key value")

class Declaration(BaseDeclaration, lessipy.tree.ruleset.Rule):
    """A declaration which has a key-value pair.

    For example, you able to use like this::

        >>> Declaration(Property("text-align"), Keyword("center")).to_css()
        'text-align: center;'
    
    Or keyword arguments also available::

        >>> Declaration(key=Property("text-align"), 
        ...             value=Keyword("center")).to_css()
        'text-align: center;'

    """


class PropertyDeclaration(Declaration):
    """A subclass for declaration which is :class:`Property`."""

    def to_css(self, context):
        key = self.key.to_css()
        try: 
            value = self.value.evaluate(context)
        except AttributeError:
            value = self.value.to_css()
        except TypeError:
            value = self.value.to_css()
        return key + ": " + value + ";"


class VariableDeclaration(Declaration):
    """A subclass for declaration which is :class:`Variable`."""

    def to_css(self, context):
        return None

