from pyke import knowledge_engine

# Create knowledge engine instance
engine = knowledge_engine.engine(__file__)

# Facts
engine.add_case_fact('facts', ('is_a', 'Fae', 'dumpus', True))

# Rules
engine.add_rule('tumpus_is_orange',
    ('is_a', '$thing', 'tumpus', True),
    ('is_orange', '$thing', True))

engine.add_rule('tumpus_is_numpus',
    ('is_a', '$thing', 'tumpus', True),
    ('is_a', '$thing', 'numpus', True))

engine.add_rule('numpus_is_small',
    ('is_a', '$thing', 'numpus', True),
    ('is_small', '$thing', True))

engine.add_rule('numpus_is_vumpus',
    ('is_a', '$thing', 'numpus', True),
    ('is_a', '$thing', 'vumpus', True))

engine.add_rule('vumpus_is_sour',
    ('is_a', '$thing', 'vumpus', True),
    ('is_sour', '$thing', True))

engine.add_rule('vumpus_is_dumpus',
    ('is_a', '$thing', 'vumpus', True),
    ('is_a', '$thing', 'dumpus', True))

engine.add_rule('dumpus_is_cold',
    ('is_a', '$thing', 'dumpus', True),
    ('is_cold', '$thing', True))

engine.add_rule('dumpus_is_zumpus',
    ('is_a', '$thing', 'dumpus', True),
    ('is_a', '$thing', 'zumpus', True))

engine.add_rule('zumpus_is_dull',
    ('is_a', '$thing', 'zumpus', True),
    ('is_dull', '$thing', True))

engine.add_rule('zumpus_is_yumpus',
    ('is_a', '$thing', 'zumpus', True),
    ('is_a', '$thing', 'yumpus', True))

engine.add_rule('jompus_is_floral',
    ('is_a', '$thing', 'jompus', True),
    ('is_floral', '$thing', True))

engine.add_rule('yumpus_is_not_amenable',
    ('is_a', '$thing', 'yumpus', True),
    ('is_amenable', '$thing', False))

engine.add_rule('yumpus_is_rompus',
    ('is_a', '$thing', 'yumpus', True),
    ('is_a', '$thing', 'rompus', True))

engine.add_rule('rompus_is_opaque',
    ('is_a', '$thing', 'rompus', True),
    ('is_opaque', '$thing', True))

engine.add_rule('rompus_is_impus',
    ('is_a', '$thing', 'rompus', True),
    ('is_a', '$thing', 'impus', True))

engine.add_rule('impus_is_not_floral',
    ('is_a', '$thing', 'impus', True),
    ('is_floral', '$thing', False))

engine.add_rule('impus_is_wumpus',
    ('is_a', '$thing', 'impus', True),
    ('is_a', '$thing', 'wumpus', True))

# Activate the knowledge base
engine.activate('rules')

# Query
result = engine.ask(('is_floral', 'Fae', False))
print("True" if result else "False")