Facts:
is_a(Wren, zumpus)

Rules:
foreach is_a($thing, tumpus)
    assert is_temperate($thing, True)

foreach is_a($thing, tumpus)
    assert is_a($thing, impus)

foreach is_a($thing, impus)
    assert is_orange($thing, True)

foreach is_a($thing, impus)
    assert is_a($thing, yumpus)

foreach is_a($thing, yumpus)
    assert is_shy($thing, True)

foreach is_a($thing, yumpus)
    assert is_a($thing, zumpus)

foreach is_a($thing, zumpus)
    assert is_bright($thing, True)

foreach is_a($thing, zumpus)
    assert is_a($thing, rompus)

foreach is_a($thing, numpus)
    assert is_opaque($thing, True)

foreach is_a($thing, rompus)
    assert is_small($thing, True)

foreach is_a($thing, rompus)
    assert is_a($thing, dumpus)

foreach is_a($thing, dumpus)
    assert not is_floral($thing, True)

foreach is_a($thing, dumpus)
    assert is_a($thing, wumpus)

foreach is_a($thing, wumpus)
    assert is_aggressive($thing, True)

foreach is_a($thing, wumpus)
    assert is_a($thing, vumpus)

foreach is_a($thing, vumpus)
    assert not is_opaque($thing, True)

foreach is_a($thing, vumpus)
    assert is_a($thing, jompus)

Query:
is_opaque(Wren, True)