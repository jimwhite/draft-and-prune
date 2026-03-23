from pyke import knowledge_engine

engine = knowledge_engine.engine(__file__)

# Add facts
engine.add_case_fact('facts', ('is_a', 'Polly', 'vumpus', True))

# Add rules
engine.add_rule('vumpus_is_zumpus',
    ('is_a', '$thing', 'vumpus', True),
    ('is_a', '$thing', 'zumpus', True))

engine.add_rule('zumpus_is_dumpus',
    ('is_a', '$thing', 'zumpus', True),
    ('is_a', '$thing', 'dumpus', True))

engine.add_rule('dumpus_is_numpus',
    ('is_a', '$thing', 'dumpus', True),
    ('is_a', '$thing', 'numpus', True))

engine.add_rule('numpus_is_tumpus',
    ('is_a', '$thing', 'numpus', True),
    ('is_a', '$thing', 'tumpus', True))

engine.add_rule('tumpus_is_not_blue',
    ('is_a', '$thing', 'tumpus', True),
    ('is_blue', '$thing', False))

# Activate the rules
engine.activate('rules')

# Query: Is Polly not blue?
result = engine.prove_1('facts', 'is_blue', ('Polly', False), 1)
print("True" if result else "False")