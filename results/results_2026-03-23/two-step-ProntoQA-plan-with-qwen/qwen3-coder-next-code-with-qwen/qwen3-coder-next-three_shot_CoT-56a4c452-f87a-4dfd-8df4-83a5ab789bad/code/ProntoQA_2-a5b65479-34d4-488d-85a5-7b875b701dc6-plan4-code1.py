# PyKe program for the tumpus logic puzzle

from pyke import knowledge_engine

# Create knowledge engine instance
engine = knowledge_engine.engine(__file__)

# Facts:
engine.add_case_fact('facts', ('is_a', 'Stella', 'yumpus', True))

# Rules:
engine.add_rule('tumpus_is_not_angry', 
    ('is_a', '$thing', 'tumpus', True),
    ('is_angry', '$thing', False))

engine.add_rule('tumpus_is_rompus', 
    ('is_a', '$thing', 'tumpus', True),
    ('is_a', '$thing', 'rompus', True))

engine.add_rule('numpus_is_not_bright', 
    ('is_a', '$thing', 'numpus', True),
    ('is_bright', '$thing', False))

engine.add_rule('rompus_is_not_luminous', 
    ('is_a', '$thing', 'rompus', True),
    ('is_luminous', '$thing', False))

engine.add_rule('rompus_is_yumpus', 
    ('is_a', '$thing', 'rompus', True),
    ('is_a', '$thing', 'yumpus', True))

engine.add_rule('yumpus_is_transparent', 
    ('is_a', '$thing', 'yumpus', True),
    ('is_transparent', '$thing', True))

engine.add_rule('yumpus_is_zumpus', 
    ('is_a', '$thing', 'yumpus', True),
    ('is_a', '$thing', 'zumpus', True))

engine.add_rule('zumpus_is_not_bitter', 
    ('is_a', '$thing', 'zumpus', True),
    ('is_bitter', '$thing', False))

engine.add_rule('zumpus_is_impus', 
    ('is_a', '$thing', 'zumpus', True),
    ('is_a', '$thing', 'impus', True))

engine.add_rule('impus_is_red', 
    ('is_a', '$thing', 'impus', True),
    ('is_red', '$thing', True))

engine.add_rule('impus_is_dumpus', 
    ('is_a', '$thing', 'impus', True),
    ('is_a', '$thing', 'dumpus', True))

engine.add_rule('dumpus_is_happy', 
    ('is_a', '$thing', 'dumpus', True),
    ('is_happy', '$thing', True))

engine.add_rule('dumpus_is_vumpus', 
    ('is_a', '$thing', 'dumpus', True),
    ('is_a', '$thing', 'vumpus', True))

engine.add_rule('vumpus_is_bright', 
    ('is_a', '$thing', 'vumpus', True),
    ('is_bright', '$thing', True))

engine.add_rule('vumpus_is_jompus', 
    ('is_a', '$thing', 'vumpus', True),
    ('is_a', '$thing', 'jompus', True))

engine.add_rule('jompus_is_large', 
    ('is_a', '$thing', 'jompus', True),
    ('is_large', '$thing', True))

engine.add_rule('jompus_is_wumpus', 
    ('is_a', '$thing', 'jompus', True),
    ('is_a', '$thing', 'wumpus', True))

# Query:
result = engine.prove(('facts', 'is_bright', 'Stella', True), 1)
print("True" if result else "False")