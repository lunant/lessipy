import lessipy.tree.cssable
import lessipy.tree.declaration


#
# + Rule # -> ruleset element
#   + Declar  # -> key/value
#     + PropertyDecl
#     + VariableDecl
#   + Ruleset


class Environment(object):

    def __init__(self, rules=()):
        self.rules = list(rules)

    def __iter__(self):
        return iter(self.rules)

    def __getitem__(self, key):
        if isinstance(key, (int, long)):
            return self.rules[key]
        for k, value in self.declarations:
            if k == key:
                return value
        raise KeyError(repr(key))

    @property
    def declarations(self):
        for rule in self:
            if isinstance(rule, tuple):
                yield rule

    def to_css(self):
        return "\n".join(rule.to_css(self) for rule in self)


class Rule(lessipy.tree.cssable.CSSable):
    """A rule."""


class UniversalRuleset(Environment, lessipy.tree.cssable.CSSable):
    """A highest ruleset."""

    def __init__(self, *rules):
        self.rules = rules

    def to_css_selector(self):
        return ""


class Ruleset(Environment, lessipy.tree.cssable.CSSable):
    """A set of rules."""

    def __init__(self, selector, *rules):
        if not isinstance(selector, lessipy.tree.selector.Selector):
            raise TypeError("selector must be a lessipy.tree.selector."
                            "Selector instance, not " + repr(selector))
        self.selector = selector
        self.parent = parent
        super(Ruleset, self).__init__(rules)

    @property
    def full_selector(self):
        return self.parent.selector + self.selector

    def to_css(self):
        selector = self.full_selector()
        body = Environment.to_css(self)


# Variable("@name"), Mixin(".name"), Property("text-align")
"""
.a {
    .b { ... }
    @var: 1px;
    a: b;
}

    Ruleset(Selector("fuck"), parent=__universal__, [
        Declaration(Property("text-align"), Keyword("left")]),
        Declaration(Variable("@height"), Measure("100", "%")),
        Declaration(Property("line-height"), Variable("@height")),
        Ruleset(Selector("you"), parent = ??, [
            Ruleset(ChildSelector("asshole"), parent = ??, [
                Declaration(Property("line-height"), Multiply(
                    Variable("@height"), Numeric("2"))
        ]),
    ]).to_css()
"""
