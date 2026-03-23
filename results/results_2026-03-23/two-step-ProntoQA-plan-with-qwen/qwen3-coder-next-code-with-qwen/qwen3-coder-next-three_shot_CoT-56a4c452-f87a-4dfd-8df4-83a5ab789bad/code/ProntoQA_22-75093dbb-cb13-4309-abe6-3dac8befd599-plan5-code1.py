Facts:
is_a(Wren, tumpus, True)

Rules:
foreach is_a($thing, wumpus, True)
    assert is_sour($thing, True)

foreach is_a($thing, wumpus, True)
    assert is_a($thing, yumpus, True)

foreach is_a($thing, yumpus, True)
    assert is_aggressive($thing, True)

foreach is_a($thing, yumpus, True)
    assert is_a($thing, tumpus, True)

foreach is_a($thing, tumpus, True)
    assert is_transparent($thing, True)

foreach is_a($thing, tumpus, True)
    assert is_a($thing, vumpus, True)

foreach is_a($thing, vumpus, True)
    assert is_wooden($thing, True)

foreach is_a($thing, vumpus, True)
    assert is_a($thing, jompus, True)

foreach is_a($thing, impus, True)
    assert not is_feisty($thing, True)

foreach is_a($thing, jompus, True)
    assert is_large($thing, True)

foreach is_a($thing, jompus, True)
    assert is_a($thing, numpus, True)

foreach is_a($thing, numpus, True)
    assert is_red($thing, True)

foreach is_a($thing, numpus, True)
    assert is_a($thing, rompus, True)

foreach is_a($thing, rompus, True)
    assert is_feisty($thing, True)

foreach is_a($thing, rompus, True)
    assert is_a($thing, zumpus, True)

Query:
is_feisty(Wren, False)