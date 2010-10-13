from lepl import *
with TraceVariables():
    ident = Regexp(r"[A-Za-z_-][A-Za-z0-9_-]+")
    spaces = Space(" \t\r\n")[1:]
    comment = Regexp(r"/\*.+?\*/") | ("//" / AnyBut("\n") / Optional("\n"))

    number = Integer() | Float()
    unit = Or("px", "em", "pc", "%", "ex", "in", "deg", "s", "pt", "cm", "mm")
    dimension = number / unit
    string_literal = String() | String(quote="'")
    url_string = Regexp(r"https?://[^)]+")
    url = Literal("url") / "(" / (string_literal | url_string) / ")"
    hex_color = Regexp(r"#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})")
    expression = Delayed()
    arguments = "(" / expression / ("," / expression)[:] / ")"
    rgb_color = "rgb" / arguments
    rgba_color = "rgba" / arguments
    hsl_color = "hsl" / arguments
    hsla_color = "hsla" / arguments
    color = hex_color | rgb_color | rgba_color | hsl_color | hsla_color
    alpha = "alpha" / arguments
    term = number | dimension | string_literal | url | color | alpha
    operator = Or("+", "-", "*", "/")
    operation = expression / operator / expression
    variable = Regexp(r"@\w+")
    expression += term | operation | variable | ("(" / expression / ")")

    node_selector = Delayed()
    universal_selector = Literal("*")
    element_selector = ident
    type_selector = universal_selector | element_selector
    id_selector = "#" & ident
    cls_selector = "." & ident
    pseudoclass_selector = ":" & ident
    property = Word()
    property_value = expression | ident
    property_decl = property / ":" / property_value
    attr_operator = Or("=", "~=", "|=")
    attr_pridicate = property / (attr_operator / property_value)[:1]
    attr_selector = "[" / attr_pridicate / "]"
    node_selector += type_selector[:1] & (id_selector | cls_selector |
                                        attr_selector | pseudoclass_selector)[:]
    child_selector = (Literals(">", "+") | Regexp(r"\s+")) / node_selector
    selector = node_selector & child_selector[:]
    selectors = selector / ("," / selector)[:]

    ruleset = Delayed()
    variable_decl = variable / ":" / expression
    declaration = (variable_decl | property_decl) / ";"
    rule = ruleset | declaration

    ruleset += selectors / "{" & (spaces[:1] / rule / spaces[:1])[:] & "}"

    import_ = "@import" // (url | string_literal) / ";"
    primary = import_ | declaration | ruleset | comment
    stylesheet = spaces[:1] / (primary / spaces[:1])[:]
