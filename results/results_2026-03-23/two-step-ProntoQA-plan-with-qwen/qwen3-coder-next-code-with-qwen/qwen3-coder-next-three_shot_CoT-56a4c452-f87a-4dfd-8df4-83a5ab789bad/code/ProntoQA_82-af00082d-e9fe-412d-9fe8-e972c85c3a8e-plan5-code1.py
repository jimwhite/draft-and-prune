facts:
    is_a(Rex, yumpus, True)

rules:
    # Each impus is a yumpus
    foreach is_a($thing, impus, True)
        assert is_a($thing, yumpus, True)

    # Yumpuses are blue
    foreach is_a($thing, yumpus, True)
        assert is_blue($thing, True)

    # Yumpuses are wumpuses
    foreach is_a($thing, yumpus, True)
        assert is_a($thing, wumpus, True)

    # Wumpuses are hot
    foreach is_a($thing, wumpus, True)
        assert is_hot($thing, True)

    # Every wumpus is a numpus
    foreach is_a($thing, wumpus, True)
        assert is_a($thing, numpus, True)

    # Jompuses are happy
    foreach is_a($thing, jompus, True)
        assert is_happy($thing, True)

    # Numpuses are fruity
    foreach is_a($thing, numpus, True)
        assert is_fruity($thing, True)

    # Numpuses are dumpuses
    foreach is_a($thing, numpus, True)
        assert is_a($thing, dumpus, True)

    # Every dumpus is not dull
    foreach is_a($thing, dumpus, True)
        assert is_dull($thing, False)

    # Every dumpus is a tumpus
    foreach is_a($thing, dumpus, True)
        assert is_a($thing, tumpus, True)

    # Tumpuses are not happy
    foreach is_a($thing, tumpus, True)
        assert is_happy($thing, False)

    # Every tumpus is a vumpus
    foreach is_a($thing, tumpus, True)
        assert is_a($thing, vumpus, True)

    # Vumpuses are not opaque
    foreach is_a($thing, vumpus, True)
        assert is_opaque($thing, False)

    # Every vumpus is a rompus
    foreach is_a($thing, vumpus, True)
        assert is_a($thing, rompus, True)

    # Rompuses are metallic
    foreach is_a($thing, rompus, True)
        assert is_metallic($thing, True)

    # Each rompus is a zumpus
    foreach is_a($thing, rompus, True)
        assert is_a($thing, zumpus, True)

query:
    facts.is_happy(Rex, False)