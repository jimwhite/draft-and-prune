Facts:
is_nice("Anne", True)

is_big("Bob", True)
is_blue("Bob", True)
is_cold("Bob", True)

is_big("Charlie", True)
is_cold("Charlie", True)
is_nice("Charlie", True)
is_young("Charlie", True)

is_furry("Fiona", True)
is_young("Fiona", True)

Rules:
# Rule: If someone is furry and nice then they are cold.
furry_and_nice_is_cold
    foreach
        is_furry($person, True)
        is_nice($person, True)
    assert
        is_cold($person, True)

# Rule: All blue and cold people are big.
blue_and_cold_are_big
    foreach
        is_blue($person, True)
        is_cold($person, True)
    assert
        is_big($person, True)

# Rule: If someone is nice then they are smart.
nice_are_smart
    foreach
        is_nice($person, True)
    assert
        is_smart($person, True)

# Rule: All smart and big people are nice.
smart_and_big_are_nice
    foreach
        is_smart($person, True)
        is_big($person, True)
    assert
        is_nice($person, True)

# Rule: All smart people are blue.
smart_are_blue
    foreach
        is_smart($person, True)
    assert
        is_blue($person, True)

# Rule: Blue, smart people are furry.
blue_and_smart_are_furry
    foreach
        is_blue($person, True)
        is_smart($person, True)
    assert
        is_furry($person, True)

# Rule: Furry, cold people are smart.
furry_and_cold_are_smart
    foreach
        is_furry($person, True)
        is_cold($person, True)
    assert
        is_smart($person, True)

# Rule: Cold people are big.
cold_are_big
    foreach
        is_cold($person, True)
    assert
        is_big($person, True)

Query:
is_smart("Charlie", False)