# Facts:
Facts:
is_a(Rex, yumpus, True)

# Rules:
Rules:
foreach is_a($thing, impus, True)
    assert is_a($thing, yumpus, True)

foreach is_a($thing, yumpus, True)
    assert is_a($thing, wumpus, True)

foreach is_a($thing, wumpus, True)
    assert is_a($thing, numpus, True)

foreach is_a($thing, numpus, True)
    assert is_a($thing, dumpus, True)

foreach is_a($thing, dumpus, True)
    assert is_a($thing, tumpus, True)

foreach is_a($thing, tumpus, True)
    assert is_happy($thing, False)

foreach is_a($thing, yumpus, True)
    assert is_blue($thing, True)

foreach is_a($thing, wumpus, True)
    assert is_hot($thing, True)

foreach is_a($thing, numpus, True)
    assert is_fruity($thing, True)

foreach is_a($thing, dumpus, True)
    assert is_dull($thing, False)

foreach is_a($thing, tumpus, True)
    assert is_a($thing, vumpus, True)

foreach is_a($thing, vumpus, True)
    assert is_opaque($thing, False)

foreach is_a($thing, vumpus, True)
    assert is_a($thing, rompus, True)

foreach is_a($thing, rompus, True)
    assert is_metallic($thing, True)

foreach is_a($thing, rompus, True)
    assert is_a($thing, zumpus, True)

foreach is_a($thing, jompus, True)
    assert is_happy($thing, True)

foreach is_a($thing, impus, True)
    assert is_mean($thing, True)

# Query:
Query:
is_happy(Rex, False)