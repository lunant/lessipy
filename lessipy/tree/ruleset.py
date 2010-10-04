import lessipy.tree.cssable
import lessipy.tree.declaration


class Environment(object):
    
    def __init__(self, declarations=None):
        self.declarations = declarations

    def to_css(self):
        body = ""
        for el in self.declarations[declaration.PropertyDeclaration]:
            body = body + "\n" + el.to_css(self)
        return body


class UniversalRuleset(Environment, lessipy.tree.cssable.CSSable):
    """A highest ruleset."""

    def __init__(self, *declarations):
        self.declarations = declarations

    def to_css_selector(self):
        return ""


class Ruleset(Environment, lessipy.tree.cssable.CSSable):
    """A set of rules."""

    def __init__(self, selector, parent, *declarations):
        if not isinstance(selector, lessipy.tree.selector.Selector):
            raise TypeError("selector must be a lessipy.tree.selector."
                            "Selector instance, not " + repr(selector))
        self.selector = selector
        self.parent = parent
        assets = {}
        for el in declarations:
            try:
                assets[el.__class__][el.key] = el
            except:
                assets[el.__class__] = {}
                assets[el.__class__][el.key] = el
        super(Ruleset, self).__init__(assets)

    @property
    def full_selector(self):
        return self.parent.selector + self.selector

    def to_css(self):
        selector = self.full_selector.to_css()
        body = Environment.to_css(self)

    def to_css_selector(self):
        self.selector.to_css()
        return self.parent.to_css_selector() + self.selector.to_css()


# Variable("@name"), Mixin(".name"), Property("text-align")
