Facts:
    is_a(Sam, wumpus, True)

Rules:
    # Tumpuses are not small
    foreach is_a($thing, tumpus, True)
        assert is_small($thing, False)
    
    # Tumpuses are yumpuses
    foreach is_a($thing, tumpus, True)
        assert is_a($thing, yumpus, True)
    
    # Every yumpus is aggressive
    foreach is_a($thing, yumpus, True)
        assert is_aggressive($thing, True)
    
    # Each yumpus is a wumpus
    foreach is_a($thing, yumpus, True)
        assert is_a($thing, wumpus, True)
    
    # Every wumpus is bright
    foreach is_a($thing, wumpus, True)
        assert is_bright($thing, True)
    
    # Each wumpus is a jompus
    foreach is_a($thing, wumpus, True)
        assert is_a($thing, jompus, True)
    
    # Jompuses are not liquid
    foreach is_a($thing, jompus, True)
        assert is_liquid($thing, False)
    
    # Every jompus is a vumpus
    foreach is_a($thing, jompus, True)
        assert is_a($thing, vumpus, True)
    
    # Each vumpus is orange
    foreach is_a($thing, vumpus, True)
        assert is_orange($thing, True)
    
    # Every vumpus is an impus
    foreach is_a($thing, vumpus, True)
        assert is_a($thing, impus, True)
    
    # Every impus is not transparent
    foreach is_a($thing, impus, True)
        assert is_transparent($thing, False)
    
    # Each impus is a zumpus
    foreach is_a($thing, impus, True)
        assert is_a($thing, zumpus, True)
    
    # Every zumpus is fruity
    foreach is_a($thing, zumpus, True)
        assert is_fruity($thing, True)
    
    # Every zumpus is a numpus
    foreach is_a($thing, zumpus, True)
        assert is_a($thing, numpus, True)
    
    # Every numpus is sour
    foreach is_a($thing, numpus, True)
        assert is_sour($thing, True)
    
    # Rompuses are not fruity
    foreach is_a($thing, rompus, True)
        assert is_fruity($thing, False)
    
    # Numpuses are dumpuses
    foreach is_a($thing, numpus, True)
        assert is_a($thing, dumpus, True)

Query:
    is_fruity(Sam, True)