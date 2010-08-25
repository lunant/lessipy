import less.tree.cssable
import less.tree.property
import less.tree.variable
import less.tree.mixin


class Declaration(less.tree.cssable.CSSable):
    """A declaration which has a key and a value.

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
            less.tree.property.Property: PropertyDeclaration,
            less.tree.variable.Variable: VariableDeclaration,
            less.tree.mixin.Mixin: MixinDeclaration,
        }
        try:
            return __map__[key.__class__](key, value)
        except KeyError:
            raise TypeError("key must be `Property` or `Variable`, `Mixin`, "
                            "passed " + repr(key))

    def to_css(self):
        return self.key.to_css() + ": " + self.value.to_css() + ";"


class PropertyDeclaration(Declaration):
    """A subclass for declaration which is :class:`Property`."""


class VariableDeclaration(Declaration):
    """A subclass for declaration which is :class:`Variable`."""

    def to_css(self):
        return None


class MixinDeclaration(Declaration):
    """A subclass for declaration which is :class:`Mixin`."""
