from lepl import *
import lessipy.tree.comment
import lessipy.tree.keyword
import lessipy.tree.dimension
import lessipy.tree.color
import lessipy.tree.numeric
import lessipy.tree.operation
import lessipy.tree.property
import lessipy.tree.string
import lessipy.tree.expression
import lessipy.tree.declaration
import lessipy.tree.rule
import lessipy.tree.variable
import lessipy.tree.ruleset
import lessipy.tree.selector
import lessipy.tree.mixin
import lessipy.tree.accessor
import lessipy.tree._import


with TraceVariables():
    spaces = Space(" \t\r\n")
    comment = Regexp(r"/\*.+?\*/") | Regexp(r"\/\/.+") >> \
                  lessipy.tree.comment.Comment
    keyword = Regexp(r"[A-Za-z_-][A-Za-z0-9_-]+") >> \
                  lessipy.tree.keyword.Keyword

    number = (Integer() | Float()) >> lessipy.tree.numeric.Numeric
    unit = Or("px", "em", "pc", "%", "ex", "in", "deg", "s", "pt", "cm", "mm")
    dimension = (number & ~Space()[:] & unit) > lessipy.tree.dimension.Dimension
    string_literal = String() | String(quote="'") >> lessipy.tree.string.String
    url_string = Regexp(r"https?://[^)]+")
    url = Literal("url") & "(" & ~Space()[:] & (string_literal | url_string) & \
          ~Space()[:] & ")"
    hex_color = Regexp(r"#[0-9A-Fa-f]{6}|#[0-9A-Fa-f]{3}") >> \
                    lessipy.tree.color.HexColor
    expression = Delayed()
    arguments = Drop("(") & ~Space()[:] & expression & ~Space()[:] & \
                (Drop(",") & ~Space()[:] & expression)[:] & ~Space()[:] & \
                Drop(")")
    rgb_color = Drop("rgb") / Drop("(") & ~Space()[:] & Integer() & \
                ~Space()[:] & (Drop(",") & ~Space()[:] & Integer())[2:2] & \
                ~Space()[:] & Drop(")") > lessipy.tree.color.RGBColor
    rgba_color = Drop("rgba") / Drop("(") & ~Space()[:] & Integer() & \
                ~Space()[:] & (Drop(",") & ~Space()[:] & Integer())[2:2] & \
                ~Space()[:] & (Drop(",") & ~Space()[:] & Float()) & \
                Drop(")") > lessipy.tree.color.RGBAColor
    hsl_color = "hsl" / arguments
    hsla_color = "hsla" / arguments
    color = hex_color | rgb_color | rgba_color | hsl_color | hsla_color
    alpha = Drop("alpha") & ~Space()[:] & Drop("(") & ~Space()[:] & \
                number & ~Space()[:] & Drop(")")
    term = Delayed()
    term += (number | dimension | string_literal | url | color | alpha |
            keyword)
    operator = Or("+", "-", "*", "/")
    operation = expression & ~Space()[:] & operator & ~Space()[:] & \
                expression > lessipy.tree.operation.Operation
    variable = Regexp(r"@[A-Za-z_-][A-Za-z0-9_-]*") \
                   >> lessipy.tree.variable.Variable
    expression += (term | operation | variable \
                  | ("(" & ~Space()[:] & expression & ~Space()[:] & ")")) & \
                  (Drop(spaces)[1:] & expression)[:] \
                      > lessipy.tree.expression.Expression
    node_selector = Delayed()

    universal_selector = Literal("*")
    element_selector = Regexp(r"[A-Za-z_-][A-Za-z0-9_-]*")
    type_selector = universal_selector | element_selector
    id_selector = Regexp(r"#[A-Za-z_-][A-Za-z0-9_-]*")
    cls_selector = Regexp(r"\.[A-Za-z_-][A-Za-z0-9_-]*")
    pseudoclass_selector = Regexp(r":[A-Za-z_-][A-Za-z0-9_-]*")

    property = Word() >> lessipy.tree.property.Property
    attr_operator = Or("=", "~=", "|=")
    attr_pridicate = property & (attr_operator & expression)[:1]
    attr_selector = Drop("[") & attr_pridicate & Drop("]")
    node_selector += type_selector[:1] & (id_selector | cls_selector |
                                        attr_selector | pseudoclass_selector)[:]
    child_selector = ~Space()[:] & (Literals(">", "+", " ")) & ~Space()[:] & \
                     node_selector & ~Space()[:]
    selector = node_selector & ~Space()[:] & child_selector[:] \
                   > lessipy.tree.selector.Selector
    selectors = selector & ~Space()[:] & (Drop(",") & ~Space()[:] & selector
                )[:] > list

    ruleset = Delayed()
    accessor = selector & Drop("[") & (variable | Drop("'") & property & \
                    Drop("'")) & Drop("]") > lessipy.tree.accessor.Accessor
    declaration = (variable | property) & ~Space()[:] & Drop(":") & \
                  ~Space()[:] & (expression | accessor) & \
                  ~Space()[:] & Drop(";") \
                    > lessipy.tree.declaration.Declaration
    mixin = Regexp(r"\.[A-Za-z_-][A-Za-z0-0_-]*") & Drop(";") \
                 > lessipy.tree.mixin.Mixin
    rule = ruleset | declaration | mixin >> lessipy.tree.rule.Rule
    rules = (rule & ~spaces[:])[:] > list

    ruleset += ~Space()[:] & selectors & ~Space()[:] & Drop("{") & ~spaces[:] \
                   & rules & Drop("}") > lessipy.tree.ruleset.Ruleset

    import_ = Drop("@import") & ~Space()[:] & (url | string_literal) & \
              Drop(";") > lessipy.tree._import.Import
    primary = import_ | declaration | ruleset | comment > list
    stylesheet = ~spaces[:1] & (primary & ~spaces[:1])[:]
