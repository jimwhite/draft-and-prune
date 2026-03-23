from pyke import knowledge_engine

# Create knowledge base
engine = knowledge_engine.engine(__file__)

# Facts section
engine.add_case_fact('facts', ('is_a', 'Rex', 'yumpus', True))

# Rules section
engine.add_rule('yumpus_is_wumpus',
    ('is_a', '$thing', 'yumpus', True),
    ('is_a', '$thing', 'wumpus', True))

engine.add_rule('wumpus_is_numpus',
    ('is_a', '$thing', 'wumpus', True),
    ('is_a', '$thing', 'numpus', True))

engine.add_rule('numpus_is_dumpus',
    ('is_a', '$thing', 'numpus', True),
    ('is_a', '$thing', 'dumpus', True))

engine.add_rule('dumpus_is_tumpus',
    ('is_a', '$thing', 'dumpus', True),
    ('is_a', '$thing', 'tumpus', True))

engine.add_rule('tumpus_is_not_happy',
    ('is_a', '$thing', 'tumpus', True),
    ('is_happy', '$thing', False))

# Query section
query_result = engine.prove(('facts', 'is_happy', 'Rex', False), 1)

# Output the result
if query_result:
    print("True")
else:
    print("False")