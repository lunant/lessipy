import lessipy.tree.cssable
import lessipy.tree.selector
import lessipy.tree.property
import lessipy.tree.variable
import lessipy.tree.mixin
import lessipy.tree.ruleset


__universal__ = lessipy.tree.ruleset.__universal__


class Declaration(lessipy.tree.ruleset.Rule, tuple):
    """A declaration which has a key-value pair.

    For example, you able to use like this::

        >>> Declaration(Property("text-align"), Keyword("center")).to_css()
        'text-align: center;'
    
    Or keyword arguments also available::

        >>> Declaration(key=Property("text-align"), 
        ...             value=Keyword("center")).to_css()
        'text-align: center;'
        
        
    """

    def __new__(cls, key, value):
        return tuple.__new__(cls, (key, value))

    @property
    def key(self):
        return self[0]

    @property
    def value(self):
        return self[1]


class PropertyDeclaration(Declaration):
    """A subclass for declaration which is :class:`Property`."""

    def to_css(self, context=__universal__):
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

    def to_css(self, context=__universal__):
        return None

