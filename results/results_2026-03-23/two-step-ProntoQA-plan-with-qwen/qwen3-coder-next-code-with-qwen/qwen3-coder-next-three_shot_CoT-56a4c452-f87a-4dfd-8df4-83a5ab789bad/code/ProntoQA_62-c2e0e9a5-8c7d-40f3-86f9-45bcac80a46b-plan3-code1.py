from pyke import knowledge_engine

engine = knowledge_engine.engine(__file__)

# Facts
engine.add_case_fact('facts', ('is_a', 'Wren', 'dumpus', True))

# Rules
engine.add_rule('zumpus_is_nervous', '''
    foreach
        facts.is_a($thing, 'zumpus', True)
    assert
        facts.is_nervous($thing, True)
''')

engine.add_rule('zumpus_is_dumpus', '''
    foreach
        facts.is_a($thing, 'dumpus', True)
    assert
        facts.is_a($thing, 'dumpus', True)
''')

engine.add_rule('dumpus_is_large', '''
    foreach
        facts.is_a($thing, 'dumpus', True)
    assert
        facts.is_large($thing, True)
''')

engine.add_rule('dumpus_is_rompus', '''
    foreach
        facts.is_a($thing, 'dumpus', True)
    assert
        facts.is_a($thing, 'rompus', True)
''')

engine.add_rule('rompus_is_brown', '''
    foreach
        facts.is_a($thing, 'rompus', True)
    assert
        facts.is_brown($thing, True)
''')

engine.add_rule('vumpus_is_transparent', '''
    foreach
        facts.is_a($thing, 'vumpus', True)
    assert
        facts.is_transparent($thing, True)
''')

engine.add_rule('rompus_is_numpus', '''
    foreach
        facts.is_a($thing, 'rompus', True)
    assert
        facts.is_a($thing, 'numpus', True)
''')

engine.add_rule('numpus_is_not_bitter', '''
    foreach
        facts.is_a($thing, 'numpus', True)
    assert
        facts.is_bitter($thing, False)
''')

engine.add_rule('numpus_is_wumpus', '''
    foreach
        facts.is_a($thing, 'numpus', True)
    assert
        facts.is_a($thing, 'wumpus', True)
''')

engine.add_rule('wumpus_is_floral', '''
    foreach
        facts.is_a($thing, 'wumpus', True)
    assert
        facts.is_floral($thing, True)
''')

engine.add_rule('wumpus_is_yumpus', '''
    foreach
        facts.is_a($thing, 'wumpus', True)
    assert
        facts.is_a($thing, 'yumpus', True)
''')

engine.add_rule('yumpus_is_not_transparent', '''
    foreach
        facts.is_a($thing, 'yumpus', True)
    assert
        facts.is_transparent($thing, False)
''')

engine.add_rule('yumpus_is_tumpus', '''
    foreach
        facts.is_a($thing, 'yumpus', True)
    assert
        facts.is_a($thing, 'tumpus', True)
''')

engine.add_rule('tumpus_is_not_bright', '''
    foreach
        facts.is_a($thing, 'tumpus', True)
    assert
        facts.is_bright($thing, False)
''')

engine.add_rule('tumpus_is_impus', '''
    foreach
        facts.is_a($thing, 'tumpus', True)
    assert
        facts.is_a($thing, 'impus', True)
''')

# Query
engine.activate('facts')
result = engine.prove_1_goal('facts.is_transparent("Wren", False)')
print(result is not None)