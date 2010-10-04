import lessipy.tree.cssable
import lessipy.tree.selector
import lessipy.tree.property
import lessipy.tree.variable
import lessipy.tree.mixin
import lessipy.tree.ruleset


__universal__ = lessipy.tree.ruleset.__universal__


class Declaration(lessipy.tree.cssable.CSSable):
    """A declaration which has a key-value pair.

    For example, you able to use like this::

        >>> Declaration(Property("text-align"), Keyword("center")).to_css()
        'text-align: center;'
    
    Or keyword arguments also available::

        >>> Declaration(key=Property("text-align"), 
        ...             value=Keyword("center")).to_css()
        'text-align: center;'
        
        
    """

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __new__(cls, key, value):
        """Before a declaration is initialized, the method catch up event and
        reassign to pre-defined subclasses.

        :param key: a :class:`Property`/:class:`Variable`/:class:`Mixin`
                    instance.
        :param value: a :class:`Expression` instance.

        If key is not a valid instance, it will raise :class:`TypeError`.


        """
        if cls is not Declaration:
            return object.__new__(cls)
        __map__ = {
            lessipy.tree.property.Property: PropertyDeclaration,
            lessipy.tree.variable.Variable: VariableDeclaration,
            lessipy.tree.selector.Selector: lessipy.tree.ruleset.Ruleset,
        }
        try:
            return __map__[key.__class__](key, value)
        except KeyError:
            raise TypeError("key must be `Property` or `Variable`, `Mixin`, "
                            "passed " + repr(key))


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


class MixinDeclaration(Declaration):
    """A subclass for declaration which is :class:`Mixin`."""

