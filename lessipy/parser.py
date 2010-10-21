from lepl import *
import lessipy.tree.css
import lessipy.tree.numeric
import lessipy.tree.color

with TraceVariables():
    spaces = Space(" \t\r\n")
    comment = Regexp(r"/\*.+?\*/") | ("//" / AnyBut("\n") / Optional("\n"))
    css_attr = Regexp(r"[A-Za-z_-][A-Za-z0-9_-]+") >> lessipy.tree.css.CSS

    number = (Integer() | Float()) >> lessipy.tree.numeric.Numeric
    unit = Or("px", "em", "pc", "%", "ex", "in", "deg", "s", "pt", "cm", "mm")
    dimension = (number & ~Space()[:] & unit) > lessipy.tree.numeric.Measure
    string_literal = String() | String(quote="'")
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
    alpha = "alpha" / arguments
    term = number | dimension | string_literal | url | color | alpha
    operator = Or("+", "-", "*", "/")
    operation = expression & ~Space()[:] & operator & ~Space()[:] & expression
    variable = Regexp(r"@[A-Za-z_-][A-Za-z0-9_-]+")
    expression += term | operation | variable | ("(" & ~Space()[:] & \
                  expression & ~Space()[:] & ")")

    node_selector = Delayed()
    universal_selector = Literal("*")
    element_selector = Regexp(r"[A-Za-z_-][A-Za-z0-9_-]+")
    type_selector = universal_selector | element_selector
    id_selector = Regexp(r"#[A-Za-z_-][A-Za-z0-9_-]+")
    cls_selector = Regexp(r"\.[A-Za-z_-][A-Za-z0-9_-]+")
    psuedoclass = Regexp(r"[A-Za-z_-][A-Za-z0-9_-]+")
    pseudoclass_selector = Drop(":") & psuedoclass
    property = Word()
    property_value = expression | css_attr
    property_decl = property & ~Space()[:] & Drop(":") & ~Space()[:] & \
                    property_value
    attr_operator = Or("=", "~=", "|=")
    attr_pridicate = property & (attr_operator & property_value)[:1]
    attr_selector = "[" & attr_pridicate & "]"
    node_selector += type_selector[:1] & (id_selector | cls_selector |
                                        attr_selector | pseudoclass_selector)[:]
    child_selector = ~Space()[:] & (Literals(">", "+", " ")) & ~Space()[:] & \
                     node_selector & ~Space()[:]
    selector = node_selector & ~Space()[:] & child_selector[:]
    selectors = selector & ~Space()[:] & ("," & ~Space()[:] & selector)[:]

    ruleset = Delayed()
    variable_decl = variable & ~Space()[:] & Drop(":") & ~Space()[:] & \
                    (expression | css_attr)
    declaration = (variable_decl | property_decl) & ~Space()[:] & Drop(";")
    rule = ruleset | declaration

    ruleset += ~Space()[:] & selectors & ~Space()[:] & Drop("{") & \
               (~spaces[:] & rule & ~spaces[:])[:] & Drop("}")

    import_ = "@import" & ~Space()[:] & (url | string_literal) & Drop(";")
    primary = import_ | declaration | ruleset | comment
    stylesheet = ~spaces[:1] & (primary & ~spaces[:1])[:]
