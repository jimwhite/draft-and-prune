Facts:
    is_a(Stella, yumpus, True)

Rules:
    # Every tumpus is not angry
    foreach is_a($thing, tumpus, True)
        assert is_angry($thing, False)

    # Tumpuses are rompuses
    foreach is_a($thing, tumpus, True)
        assert is_a($thing, rompus, True)

    # Every numpus is not bright
    foreach is_a($thing, numpus, True)
        assert is_bright($thing, False)

    # Rompuses are not luminous
    foreach is_a($thing, rompus, True)
        assert is_luminous($thing, False)

    # Rompuses are yumpuses
    foreach is_a($thing, rompus, True)
        assert is_a($thing, yumpus, True)

    # Yumpuses are transparent
    foreach is_a($thing, yumpus, True)
        assert is_transparent($thing, True)

    # Yumpuses are zumpuses
    foreach is_a($thing, yumpus, True)
        assert is_a($thing, zumpus, True)

    # Each zumpus is not bitter
    foreach is_a($thing, zumpus, True)
        assert is_bitter($thing, False)

    # Zumpuses are impuses
    foreach is_a($thing, zumpus, True)
        assert is_a($thing, impus, True)

    # Impuses are red
    foreach is_a($thing, impus, True)
        assert is_red($thing, True)

    # Each impus is a dumpus
    foreach is_a($thing, impus, True)
        assert is_a($thing, dumpus, True)

    # Every dumpus is happy
    foreach is_a($thing, dumpus, True)
        assert is_happy($thing, True)

    # Each dumpus is a vumpus
    foreach is_a($thing, dumpus, True)
        assert is_a($thing, vumpus, True)

    # Vumpuses are bright
    foreach is_a($thing, vumpus, True)
        assert is_bright($thing, True)

    # Every vumpus is a jompus
    foreach is_a($thing, vumpus, True)
        assert is_a($thing, jompus, True)

    # Jompuses are large
    foreach is_a($thing, jompus, True)
        assert is_large($thing, True)

    # Each jompus is a wumpus
    foreach is_a($thing, jompus, True)
        assert is_a($thing, wumpus, True)

Query:
    is_bright(Stella, True)