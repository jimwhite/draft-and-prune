from pyke import knowledge_engine

engine = knowledge_engine.engine(__file__)

# Facts section
engine.add_assertion(('is_a', 'Sally', 'wumpus', True))

# Rules section
engine.add_rule('wumpus_is_dumpus',
    ('is_a', '$thing', 'wumpus', True),
    ('is_a', '$thing', 'dumpus', True))

engine.add_rule('dumpus_is_zumpus',
    ('is_a', '$thing', 'dumpus', True),
    ('is_a', '$thing', 'zumpus', True))

engine.add_rule('zumpus_is_rompus',
    ('is_a', '$thing', 'zumpus', True),
    ('is_a', '$thing', 'rompus', True))

engine.add_rule('rompus_is_impus',
    ('is_a', '$thing', 'rompus', True),
    ('is_a', '$thing', 'impus', True))

engine.add_rule('impus_is_metallic',
    ('is_a', '$thing', 'impus', True),
    ('is_metallic', '$thing', True))

# Query section
result = engine.prove(('is_metallic', 'Sally', True), 1)
print("True" if result else "False")