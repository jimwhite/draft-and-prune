# Import required modules
from pyke import knowledge_engine

# Create knowledge engine instance
engine = knowledge_engine.engine(__file__)

# Facts section
engine.add_universal_fact('facts', 'is_a', ('Sally', 'numpus', True))

# Rules section
engine.add_rule('numpus_is_earthy',
    ('facts', 'is_a', '$thing', 'numpus', True),
    ('facts', 'is_earthy', '$thing', True))

engine.add_rule('numpus_is_vumpus',
    ('facts', 'is_a', '$thing', 'numpus', True),
    ('facts', 'is_a', '$thing', 'vumpus', True))

engine.add_rule('vumpus_is_transparent',
    ('facts', 'is_a', '$thing', 'vumpus', True),
    ('facts', 'is_transparent', '$thing', True))

engine.add_rule('vumpus_is_tumpus',
    ('facts', 'is_a', '$thing', 'vumpus', True),
    ('facts', 'is_a', '$thing', 'tumpus', True))

engine.add_rule('tumpus_is_small',
    ('facts', 'is_a', '$thing', 'tumpus', True),
    ('facts', 'is_small', '$thing', True))

engine.add_rule('tumpus_is_dumpus',
    ('facts', 'is_a', '$thing', 'tumpus', True),
    ('facts', 'is_a', '$thing', 'dumpus', True))

engine.add_rule('dumpus_is_not_aggressive',
    ('facts', 'is_a', '$thing', 'dumpus', True),
    ('facts', 'is_aggressive', '$thing', False))

engine.add_rule('dumpus_is_wumpus',
    ('facts', 'is_a', '$thing', 'dumpus', True),
    ('facts', 'is_a', '$thing', 'wumpus', True))

engine.add_rule('wumpus_is_not_wooden',
    ('facts', 'is_a', '$thing', 'wumpus', True),
    ('facts', 'is_wooden', '$thing', False))

engine.add_rule('wumpus_is_jompus',
    ('facts', 'is_a', '$thing', 'wumpus', True),
    ('facts', 'is_a', '$thing', 'jompus', True))

engine.add_rule('jompus_is_not_nervous',
    ('facts', 'is_a', '$thing', 'jompus', True),
    ('facts', 'is_nervous', '$thing', False))

engine.add_rule('jompus_is_zumpus',
    ('facts', 'is_a', '$thing', 'jompus', True),
    ('facts', 'is_a', '$thing', 'zumpus', True))

engine.add_rule('zumpus_is_temperate',
    ('facts', 'is_a', '$thing', 'zumpus', True),
    ('facts', 'is_temperate', '$thing', True))

engine.add_rule('rompus_is_wooden',
    ('facts', 'is_a', '$thing', 'rompus', True),
    ('facts', 'is_wooden', '$thing', True))

engine.add_rule('zumpus_is_impus',
    ('facts', 'is_a', '$thing', 'zumpus', True),
    ('facts', 'is_a', '$thing', 'impus', True))

engine.add_rule('impus_is_blue',
    ('facts', 'is_a', '$thing', 'impus', True),
    ('facts', 'is_blue', '$thing', True))

engine.add_rule('impus_is_yumpus',
    ('facts', 'is_a', '$thing', 'impus', True),
    ('facts', 'is_a', '$thing', 'yumpus', True))

# Query section
engine.activate('facts')

# Prove the statement: Sally is not wooden
result = engine.prove(('facts', 'is_wooden', 'Sally', False), 1)

print("Statement 'Sally is not wooden' is:", result is not None)