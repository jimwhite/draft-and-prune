Facts:
is_a(Max, numpus, True)

Rules:
foreach is_a($thing, rompus, True)
    assert is_large($thing, False)

foreach is_a($thing, rompus, True)
    assert is_a($thing, numpus, True)

foreach is_a($thing, numpus, True)
    assert is_fruity($thing, True)

foreach is_a($thing, numpus, True)
    assert is_a($thing, wumpus, True)

foreach is_a($thing, wumpus, True)
    assert is_metallic($thing, False)

foreach is_a($thing, wumpus, True)
    assert is_a($thing, tumpus, True)

foreach is_a($thing, tumpus, True)
    assert is_cold($thing, True)

foreach is_a($thing, dumpus, True)
    assert is_brown($thing, False)

foreach is_a($thing, tumpus, True)
    assert is_a($thing, jompus, True)

foreach is_a($thing, jompus, True)
    assert is_sweet($thing, True)

foreach is_a($thing, jompus, True)
    assert is_a($thing, zumpus, True)

foreach is_a($thing, zumpus, True)
    assert is_brown($thing, True)

foreach is_a($thing, zumpus, True)
    assert is_a($thing, yumpus, True)

Query:
is_brown(Max, False)