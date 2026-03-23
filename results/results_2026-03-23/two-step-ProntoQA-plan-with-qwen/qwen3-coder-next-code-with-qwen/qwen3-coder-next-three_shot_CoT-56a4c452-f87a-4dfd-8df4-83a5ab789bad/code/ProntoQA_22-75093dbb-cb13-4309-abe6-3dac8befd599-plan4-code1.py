from pyke import knowledge_engine

# Initialize the knowledge engine
engine = knowledge_engine.engine(__file__)

# Facts:
engine.add_case_fact('facts', ('is_a', 'Wren', 'tumpus', True))

# Rules:
engine.add_rule('wumpus_is_sour', '''
    foreach facts.is_a($thing, 'wumpus', True)
    assert facts.is_sour($thing, True)
''')

engine.add_rule('wumpus_is_yumpus', '''
    foreach facts.is_a($thing, 'wumpus', True)
    assert facts.is_a($thing, 'yumpus', True)
''')

engine.add_rule('yumpus_is_aggressive', '''
    foreach facts.is_a($thing, 'yumpus', True)
    assert facts.is_aggressive($thing, True)
''')

engine.add_rule('yumpus_is_tumpus', '''
    foreach facts.is_a($thing, 'yumpus', True)
    assert facts.is_a($thing, 'tumpus', True)
''')

engine.add_rule('tumpus_is_transparent', '''
    foreach facts.is_a($thing, 'tumpus', True)
    assert facts.is_transparent($thing, True)
''')

engine.add_rule('tumpus_is_vumpus', '''
    foreach facts.is_a($thing, 'tumpus', True)
    assert facts.is_a($thing, 'vumpus', True)
''')

engine.add_rule('vumpus_is_wooden', '''
    foreach facts.is_a($thing, 'vumpus', True)
    assert facts.is_wooden($thing, True)
''')

engine.add_rule('vumpus_is_jompus', '''
    foreach facts.is_a($thing, 'vumpus', True)
    assert facts.is_a($thing, 'jompus', True)
''')

engine.add_rule('impus_is_not_feisty', '''
    foreach facts.is_a($thing, 'impus', True)
    assert facts.is_feisty($thing, False)
''')

engine.add_rule('jompus_is_large', '''
    foreach facts.is_a($thing, 'jompus', True)
    assert facts.is_large($thing, True)
''')

engine.add_rule('jompus_is_numpus', '''
    foreach facts.is_a($thing, 'jompus', True)
    assert facts.is_a($thing, 'numpus', True)
''')

engine.add_rule('numpus_is_red', '''
    foreach facts.is_a($thing, 'numpus', True)
    assert facts.is_red($thing, True)
''')

engine.add_rule('numpus_is_rompus', '''
    foreach facts.is_a($thing, 'numpus', True)
    assert facts.is_a($thing, 'rompus', True)
''')

engine.add_rule('rompus_is_feisty', '''
    foreach facts.is_a($thing, 'rompus', True)
    assert facts.is_feisty($thing, True)
''')

engine.add_rule('rompus_is_zumpus', '''
    foreach facts.is_a($thing, 'rompus', True)
    assert facts.is_a($thing, 'zumpus', True)
''')

# Query:
engine.activate('facts')
result = engine.prove('facts', 'is_feisty', ('Wren', False), 1)

# Output the result
if result:
    print("True")
else:
    print("False")