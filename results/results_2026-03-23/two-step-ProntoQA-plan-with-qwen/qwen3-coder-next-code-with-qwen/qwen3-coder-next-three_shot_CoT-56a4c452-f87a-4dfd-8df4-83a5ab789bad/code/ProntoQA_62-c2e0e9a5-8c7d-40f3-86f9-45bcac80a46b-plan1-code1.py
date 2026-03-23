Facts:
is_a(Wren, dumpus, True)

Rules:
foreach is_a(?x, zumpus, True)
    assert is_nervous(?x, True)

foreach is_a(?x, dumpus, True)
    assert is_large(?x, True)

foreach is_a(?x, dumpus, True)
    assert is_a(?x, rompus, True)

foreach is_a(?x, rompus, True)
    assert is_brown(?x, True)

foreach is_a(?x, vumpus, True)
    assert is_transparent(?x, True)

foreach is_a(?x, rompus, True)
    assert is_a(?x, numpus, True)

foreach is_a(?x, numpus, True)
    assert not is_bitter(?x, True)

foreach is_a(?x, numpus, True)
    assert is_a(?x, wumpus, True)

foreach is_a(?x, wumpus, True)
    assert is_floral(?x, True)

foreach is_a(?x, wumpus, True)
    assert is_a(?x, yumpus, True)

foreach is_a(?x, yumpus, True)
    assert not is_transparent(?x, True)

foreach is_a(?x, yumpus, True)
    assert is_a(?x, tumpus, True)

foreach is_a(?x, tumpus, True)
    assert not is_bright(?x, True)

foreach is_a(?x, tumpus, True)
    assert is_a(?x, impus, True)

Query:
is_transparent(Wren, False)