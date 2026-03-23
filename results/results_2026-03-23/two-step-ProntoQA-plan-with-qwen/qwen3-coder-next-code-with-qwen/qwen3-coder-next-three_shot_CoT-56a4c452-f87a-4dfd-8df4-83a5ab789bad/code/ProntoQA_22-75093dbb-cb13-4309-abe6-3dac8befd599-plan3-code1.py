# Facts
is_a("Wren", "tumpus", True)

# Rules
wumpus_is_sour:
    foreach is_a($thing, "wumpus", True)
    assert is_sour($thing, True)

wumpus_is_yumpus:
    foreach is_a($thing, "wumpus", True)
    assert is_a($thing, "yumpus", True)

yumpus_is_aggressive:
    foreach is_a($thing, "yumpus", True)
    assert is_aggressive($thing, True)

yumpus_is_tumpus:
    foreach is_a($thing, "yumpus", True)
    assert is_a($thing, "tumpus", True)

tumpus_is_transparent:
    foreach is_a($thing, "tumpus", True)
    assert is_transparent($thing, True)

tumpus_is_vumpus:
    foreach is_a($thing, "tumpus", True)
    assert is_a($thing, "vumpus", True)

vumpus_is_wooden:
    foreach is_a($thing, "vumpus", True)
    assert is_wooden($thing, True)

vumpus_is_jompus:
    foreach is_a($thing, "vumpus", True)
    assert is_a($thing, "jompus", True)

impus_is_not_feisty:
    foreach is_a($thing, "impus", True)
    assert is_feisty($thing, False)

jompus_is_large:
    foreach is_a($thing, "jompus", True)
    assert is_large($thing, True)

jompus_is_numpus:
    foreach is_a($thing, "jompus", True)
    assert is_a($thing, "numpus", True)

numpus_is_red:
    foreach is_a($thing, "numpus", True)
    assert is_red($thing, True)

numpus_is_rompus:
    foreach is_a($thing, "numpus", True)
    assert is_a($thing, "rompus", True)

rompus_is_feisty:
    foreach is_a($thing, "rompus", True)
    assert is_feisty($thing, True)

rompus_is_zumpus:
    foreach is_a($thing, "rompus", True)
    assert is_a($thing, "zumpus", True)

# Query
is_feisty("Wren", False)