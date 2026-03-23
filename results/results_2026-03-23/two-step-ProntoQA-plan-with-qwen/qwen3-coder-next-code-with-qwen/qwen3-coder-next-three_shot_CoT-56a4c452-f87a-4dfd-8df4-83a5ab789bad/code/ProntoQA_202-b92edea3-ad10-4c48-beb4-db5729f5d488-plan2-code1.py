from pyke import knowledge_engine

# Create knowledge engine instance
engine = knowledge_engine.engine(__file__)

# Facts
engine.add_case_fact('facts', ('is_a', 'Wren', 'zumpus', True))

# Rules
engine.add_rule('tumpus_is_temperate', 
    ('is_a', '$thing', 'tumpus', True),
    ('is_temperate', '$thing', True))

engine.add_rule('tumpus_is_impus',
    ('is_a', '$thing', 'tumpus', True),
    ('is_a', '$thing', 'impus', True))

engine.add_rule('impus_is_orange',
    ('is_a', '$thing', 'impus', True),
    ('is_orange', '$thing', True))

engine.add_rule('impus_is_yumpus',
    ('is_a', '$thing', 'impus', True),
    ('is_a', '$thing', 'yumpus', True))

engine.add_rule('yumpus_is_shy',
    ('is_a', '$thing', 'yumpus', True),
    ('is_shy', '$thing', True))

engine.add_rule('yumpus_is_zumpus',
    ('is_a', '$thing', 'yumpus', True),
    ('is_a', '$thing', 'zumpus', True))

engine.add_rule('zumpus_is_bright',
    ('is_a', '$thing', 'zumpus', True),
    ('is_bright', '$thing', True))

engine.add_rule('zumpus_is_rompus',
    ('is_a', '$thing', 'zumpus', True),
    ('is_a', '$thing', 'rompus', True))

engine.add_rule('numpus_is_opaque',
    ('is_a', '$thing', 'numpus', True),
    ('is_opaque', '$thing', True))

engine.add_rule('rompus_is_small',
    ('is_a', '$thing', 'rompus', True),
    ('is_small', '$thing', True))

engine.add_rule('rompus_is_dumpus',
    ('is_a', '$thing', 'rompus', True),
    ('is_a', '$thing', 'dumpus', True))

engine.add_rule('dumpus_is_not_floral',
    ('is_a', '$thing', 'dumpus', True),
    ('is_floral', '$thing', False))

engine.add_rule('dumpus_is_wumpus',
    ('is_a', '$thing', 'dumpus', True),
    ('is_a', '$thing', 'wumpus', True))

engine.add_rule('wumpus_is_aggressive',
    ('is_a', '$thing', 'wumpus', True),
    ('is_aggressive', '$thing', True))

engine.add_rule('wumpus_is_vumpus',
    ('is_a', '$thing', 'wumpus', True),
    ('is_a', '$thing', 'vumpus', True))

engine.add_rule('vumpus_is_not_opaque',
    ('is_a', '$thing', 'vumpus', True),
    ('is_opaque', '$thing', False))

engine.add_rule('vumpus_is_jompus',
    ('is_a', '$thing', 'vumpus', True),
    ('is_a', '$thing', 'jompus', True))

# Activate rules and run
engine.activate('rules')

# Query: Is Wren opaque?
result = engine.query(('is_opaque', 'Wren', True))