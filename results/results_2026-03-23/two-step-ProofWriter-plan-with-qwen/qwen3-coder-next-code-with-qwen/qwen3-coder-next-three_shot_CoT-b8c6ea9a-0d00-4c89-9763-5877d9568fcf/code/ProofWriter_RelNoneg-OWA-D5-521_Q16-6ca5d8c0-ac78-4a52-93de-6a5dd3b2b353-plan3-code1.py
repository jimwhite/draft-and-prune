# PyKe knowledge base file

Facts:
eats(cow, lion, True)
eats(lion, mouse, True)
needs(lion, mouse, True)
sees(mouse, lion, True)
eats(tiger, lion, True)
is_green(tiger, True)
is_red(tiger, True)
needs(tiger, lion, True)
needs(tiger, mouse, True)
sees(tiger, cow, True)
sees(cow, lion, True)

Rules:
# If someone sees the lion then they are cold
sees_lion_is_cold:
    foreach sees($person, lion, True)
    assert is_cold($person, True)

# If someone needs the tiger and they need the mouse then they are cold
needs_tiger_and_mouse_is_cold:
    foreach needs($person, tiger, True)
           needs($person, mouse, True)
    assert is_cold($person, True)

# If someone needs the tiger and the tiger eats the cow then the tiger needs the lion
needs_tiger_and_tiger_eats_cow:
    foreach needs($person, tiger, True)
           eats(tiger, cow, True)
    assert needs(tiger, lion, True)

# All round people are green
round_are_green:
    foreach is_round($person, True)
    assert is_green($person, True)

# All young, green people are round
young_and_green_are_round:
    foreach is_young($person, True)
           is_green($person, True)
    assert is_round($person, True)

# If someone eats the mouse and the mouse sees the lion then they are green
eats_mouse_and_mouse_sees_lion_is_green:
    foreach eats($person, mouse, True)
           sees(mouse, lion, True)
    assert is_green($person, True)

# If someone needs the tiger then the tiger sees the lion
needs_tiger_tiger_sees_lion:
    foreach needs($person, tiger, True)
    assert sees(tiger, lion, True)

# If someone is cold and they see the lion then they need the tiger
cold_and_sees_lion_needs_tiger:
    foreach is_cold($person, True)
           sees($person, lion, True)
    assert needs($person, tiger, True)

Query:
needs(cow, tiger, True)