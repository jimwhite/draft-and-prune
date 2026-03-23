from pyke import knowledge_engine

engine = knowledge_engine.engine(__file__)

# Facts - using add_fact for direct assertions
engine.add_fact('facts', 'is_a', ('Wren', 'vumpus'))

# Rules - using foreach and assert for inference rules
engine.add_rule('tumpus_is_dull',
    ('is_a', '$thing', 'tumpus'),
    ('is_dull', '$thing'))

engine.add_rule('tumpus_is_jompus',
    ('is_a', '$thing', 'tumpus'),
    ('is_a', '$thing', 'jompus'))

engine.add_rule('jompus_is_not_sour',
    ('is_a', '$thing', 'jompus'),
    ('is_sour', '$thing', False))

engine.add_rule('jompus_is_vumpus',
    ('is_a', '$thing', 'jompus'),
    ('is_a', '$thing', 'vumpus'))

engine.add_rule('vumpus_is_feisty',
    ('is_a', '$thing', 'vumpus'),
    ('is_feisty', '$thing'))

engine.add_rule('vumpus_is_dumpus',
    ('is_a', '$thing', 'vumpus'),
    ('is_a', '$thing', 'dumpus'))

engine.add_rule('dumpus_is_cold',
    ('is_a', '$thing', 'dumpus'),
    ('is_cold', '$thing'))

engine.add_rule('dumpus_is_yumpus',
    ('is_a', '$thing', 'dumpus'),
    ('is_a', '$thing', 'yumpus'))

engine.add_rule('yumpus_is_transparent',
    ('is_a', '$thing', 'yumpus'),
    ('is_transparent', '$thing'))

engine.add_rule('yumpus_is_numpus',
    ('is_a', '$thing', 'yumpus'),
    ('is_a', '$thing', 'numpus'))

engine.add_rule('numpus_is_not_amenable',
    ('is_a', '$thing', 'numpus'),
    ('is_amenable', '$thing', False))

engine.add_rule('numpus_is_zumpus',
    ('is_a', '$thing', 'numpus'),
    ('is_a', '$thing', 'zumpus'))

engine.add_rule('zumpus_is_orange',
    ('is_a', '$thing', 'zumpus'),
    ('is_orange', '$thing'))

engine.add_rule('zumpus_is_rompus',
    ('is_a', '$thing', 'zumpus'),
    ('is_a', '$thing', 'rompus'))

engine.add_rule('rompus_is_earthy',
    ('is_a', '$thing', 'rompus'),
    ('is_earthy', '$thing'))

engine.add_rule('impus_is_not_orange',
    ('is_a', '$thing', 'impus'),
    ('is_orange', '$thing', False))

engine.add_rule('rompus_is_wumpus',
    ('is_a', '$thing', 'rompus'),
    ('is_a', '$thing', 'wumpus'))

# Query: Is Wren not orange?
# First, let's check if Wren is orange (should be true based on the chain)
try:
    # Prove that Wren is orange
    result_orange = engine.prove_1('facts', 'is_orange', ('Wren',), 1)
    wren_is_orange = True
except:
    wren_is_orange = False

# The statement "Wren is not orange" is true if wren_is_orange is False
result = not wren_is_orange

print(result)