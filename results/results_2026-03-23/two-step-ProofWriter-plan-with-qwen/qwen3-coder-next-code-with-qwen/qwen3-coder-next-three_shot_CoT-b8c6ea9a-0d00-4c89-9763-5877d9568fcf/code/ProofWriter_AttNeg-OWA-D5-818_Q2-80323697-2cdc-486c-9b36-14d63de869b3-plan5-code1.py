# Facts:
is_young("Charlie", True)
is_blue("Erin", True)
is_kind("Erin", False)
is_blue("Fiona", True)
is_white("Fiona", True)
is_blue("Gary", True)
is_kind("Gary", True)

# Rules:
# Furry, nice things are white.
rule1 = (
    (lambda x: is_furry(x, True) and is_nice(x, True)),
    lambda x: is_white(x, True)
)

# If something is young and blue then it is smart.
rule2 = (
    (lambda x: is_young(x, True) and is_blue(x, True)),
    lambda x: is_smart(x, True)
)

# All blue, smart things are furry.
rule3 = (
    (lambda x: is_blue(x, True) and is_smart(x, True)),
    lambda x: is_furry(x, True)
)

# All smart, white things are furry.
rule4 = (
    (lambda x: is_smart(x, True) and is_white(x, True)),
    lambda x: is_furry(x, True)
)

# Young things are nice.
rule5 = (
    (lambda x: is_young(x, True)),
    lambda x: is_nice(x, True)
)

# If Fiona is smart and Fiona is young then Fiona is not furry.
rule6 = (
    (lambda: is_smart("Fiona", True) and is_young("Fiona", True)),
    lambda: is_furry("Fiona", False)
)

# If Erin is kind then Erin is furry.
rule7 = (
    (lambda: is_kind("Erin", True)),
    lambda: is_furry("Erin", True)
)

# If Gary is smart and Gary is white then Gary is not kind.
rule8 = (
    (lambda: is_smart("Gary", True) and is_white("Gary", True)),
    lambda: is_kind("Gary", False)
)

# If something is nice then it is blue.
rule9 = (
    (lambda x: is_nice(x, True)),
    lambda x: is_blue(x, True)
)

# Query:
is_white("Fiona", False)