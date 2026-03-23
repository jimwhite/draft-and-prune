from pyke import knowledge_engine

engine = knowledge_engine.engine(__file__)

# Facts
engine.add_rule('facts', 'is_a', ('Wren', 'yumpus', True))

# Rules - using proper PyKe syntax with foreach and assert
engine.add_rule('jompus_is_bright',
    ('is_a', '$thing', 'jompus'),
    ('is_bright', '$thing'))

engine.add_rule('jompus_is_vumpus',
    ('is_a', '$thing', 'jompus'),
    ('is_a', '$thing', 'vumpus'))

engine.add_rule('vumpus_is_floral',
    ('is_a', '$thing', 'vumpus'),
    ('is_floral', '$thing'))

engine.add_rule('vumpus_is_yumpus',
    ('is_a', '$thing', 'vumpus'),
    ('is_a', '$thing', 'yumpus'))

engine.add_rule('yumpus_is_not_temperate',
    ('is_a', '$thing', 'yumpus'),
    ('not', ('is_temperate', '$thing')))

engine.add_rule('yumpus_is_numpus',
    ('is_a', '$thing', 'yumpus'),
    ('is_a', '$thing', 'numpus'))

engine.add_rule('numpus_is_sweet',
    ('is_a', '$thing', 'numpus'),
    ('is_sweet', '$thing'))

engine.add_rule('numpus_is_zumpus',
    ('is_a', '$thing', 'numpus'),
    ('is_a', '$thing', 'zumpus'))

engine.add_rule('zumpus_is_mean',
    ('is_a', '$thing', 'zumpus'),
    ('is_mean', '$thing'))

engine.add_rule('zumpus_is_rompus',
    ('is_a', '$thing', 'zumpus'),
    ('is_a', '$thing', 'rompus'))

engine.add_rule('rompus_is_not_feisty',
    ('is_a', '$thing', 'rompus'),
    ('not', ('is_feisty', '$thing')))

engine.add_rule('impus_is_not_transparent',
    ('is_a', '$thing', 'impus'),
    ('not', ('is_transparent', '$thing')))

engine.add_rule('rompus_is_wumpus',
    ('is_a', '$thing', 'rompus'),
    ('is_a', '$thing', 'wumpus'))

engine.add_rule('wumpus_is_transparent',
    ('is_a', '$thing', 'wumpus'),
    ('is_transparent', '$thing'))

engine.add_rule('wumpus_is_dumpus',
    ('is_a', '$thing', 'wumpus'),
    ('is_a', '$thing', 'dumpus'))

engine.add_rule('dumpus_is_large',
    ('is_a', '$thing', 'dumpus'),
    ('is_large', '$thing'))

engine.add_rule('dumpus_is_tumpus',
    ('is_a', '$thing', 'dumpus'),
    ('is_a', '$thing', 'tumpus'))

# Activate the knowledge base
engine.activate('facts')

# Query: Is Wren transparent?
result = engine.prove_1('facts', 'is_transparent', ('Wren',), 1)
print("True" if result else "False")