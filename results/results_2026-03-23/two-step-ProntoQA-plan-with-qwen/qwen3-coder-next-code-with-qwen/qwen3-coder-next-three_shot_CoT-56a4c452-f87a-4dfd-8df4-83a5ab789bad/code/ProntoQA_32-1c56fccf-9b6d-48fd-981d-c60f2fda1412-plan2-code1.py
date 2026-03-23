# Facts, Rules, and Query for PyKe

from pyke import knowledge_engine

engine = knowledge_engine.engine(__file__)

# Facts
engine.add_rule('facts', '''
    is_a("Sally", "numpus", True)
''')

# Rules
engine.add_rule('facts', '''
    # Numpuses are earthy.
    numpus_is_earthy
        foreach
            facts.is_a($thing, "numpus", True)
        assert
            facts.is_earthy($thing, True)
''')

engine.add_rule('facts', '''
    # Numpuses are vumpuses.
    numpus_is_vumpus
        foreach
            facts.is_a($thing, "numpus", True)
        assert
            facts.is_a($thing, "vumpus", True)
''')

engine.add_rule('facts', '''
    # Vumpuses are transparent.
    vumpus_is_transparent
        foreach
            facts.is_a($thing, "vumpus", True)
        assert
            facts.is_transparent($thing, True)
''')

engine.add_rule('facts', '''
    # Each vumpus is a tumpus.
    vumpus_is_tumpus
        foreach
            facts.is_a($thing, "vumpus", True)
        assert
            facts.is_a($thing, "tumpus", True)
''')

engine.add_rule('facts', '''
    # Tumpuses are small.
    tumpus_is_small
        foreach
            facts.is_a($thing, "tumpus", True)
        assert
            facts.is_small($thing, True)
''')

engine.add_rule('facts', '''
    # Tumpuses are dumpuses.
    tumpus_is_dumpus
        foreach
            facts.is_a($thing, "tumpus", True)
        assert
            facts.is_a($thing, "dumpus", True)
''')

engine.add_rule('facts', '''
    # Each dumpus is not aggressive.
    dumpus_is_not_aggressive
        foreach
            facts.is_a($thing, "dumpus", True)
        assert
            facts.is_aggressive($thing, False)
''')

engine.add_rule('facts', '''
    # Dumpuses are wumpuses.
    dumpus_is_wumpus
        foreach
            facts.is_a($thing, "dumpus", True)
        assert
            facts.is_a($thing, "wumpus", True)
''')

engine.add_rule('facts', '''
    # Every wumpus is not wooden.
    wumpus_is_not_wooden
        foreach
            facts.is_a($thing, "wumpus", True)
        assert
            facts.is_wooden($thing, False)
''')

engine.add_rule('facts', '''
    # Every wumpus is a jompus.
    wumpus_is_jompus
        foreach
            facts.is_a($thing, "wumpus", True)
        assert
            facts.is_a($thing, "jompus", True)
''')

engine.add_rule('facts', '''
    # Jompuses are not nervous.
    jompus_is_not_nervous
        foreach
            facts.is_a($thing, "jompus", True)
        assert
            facts.is_nervous($thing, False)
''')

engine.add_rule('facts', '''
    # Each jompus is a zumpus.
    jompus_is_zumpus
        foreach
            facts.is_a($thing, "jompus", True)
        assert
            facts.is_a($thing, "zumpus", True)
''')

engine.add_rule('facts', '''
    # Each zumpus is temperate.
    zumpus_is_temperate
        foreach
            facts.is_a($thing, "zumpus", True)
        assert
            facts.is_temperate($thing, True)
''')

engine.add_rule('facts', '''
    # Rompuses are wooden.
    rompus_is_wooden
        foreach
            facts.is_a($thing, "rompus", True)
        assert
            facts.is_wooden($thing, True)
''')

engine.add_rule('facts', '''
    # Zumpuses are impuses.
    zumpus_is_impus
        foreach
            facts.is_a($thing, "zumpus", True)
        assert
            facts.is_a($thing, "impus", True)
''')

engine.add_rule('facts', '''
    # Each impus is blue.
    impus_is_blue
        foreach
            facts.is_a($thing, "impus", True)
        assert
            facts.is_blue($thing, True)
''')

engine.add_rule('facts', '''
    # Impuses are yumpuses.
    impus_is_yumpus
        foreach
            facts.is_a($thing, "impus", True)
        assert
            facts.is_a($thing, "yumpus", True)
''')

# Query: Is Sally not wooden?
# We need to prove that is_wooden("Sally", False) holds
engine.activate_rule('facts')
result = engine.prove('facts.is_wooden("Sally", False)', 1)
print(result[0] if result else False)