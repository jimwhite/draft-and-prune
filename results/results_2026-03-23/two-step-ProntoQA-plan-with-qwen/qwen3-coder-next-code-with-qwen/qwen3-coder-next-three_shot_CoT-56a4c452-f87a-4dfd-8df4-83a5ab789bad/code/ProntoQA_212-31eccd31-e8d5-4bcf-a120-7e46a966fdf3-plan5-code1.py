from pyke import knowledge_engine

engine = knowledge_engine.engine(__file__)

# Facts section
engine.add_case_fact('facts', ('is_a', 'Stella', 'wumpus', True))

# Rules section
engine.add_rule('tumpus_is_red', 
    ('is_a', '$thing', 'tumpus', True),
    ('is_red', '$thing', True))

engine.add_rule('tumpus_is_wumpus', 
    ('is_a', '$thing', 'tumpus', True),
    ('is_a', '$thing', 'wumpus', True))

engine.add_rule('wumpus_is_sweet', 
    ('is_a', '$thing', 'wumpus', True),
    ('is_sweet', '$thing', True))

engine.add_rule('wumpus_is_vumpus', 
    ('is_a', '$thing', 'wumpus', True),
    ('is_a', '$thing', 'vumpus', True))

engine.add_rule('vumpus_is_small', 
    ('is_a', '$thing', 'vumpus', True),
    ('is_small', '$thing', True))

engine.add_rule('vumpus_is_jompus', 
    ('is_a', '$thing', 'vumpus', True),
    ('is_a', '$thing', 'jompus', True))

engine.add_rule('jompus_is_not_aggressive', 
    ('is_a', '$thing', 'jompus', True),
    ('is_aggressive', '$thing', False))

engine.add_rule('zumpus_is_temperate', 
    ('is_a', '$thing', 'zumpus', True),
    ('is_temperate', '$thing', True))

engine.add_rule('jompus_is_dumpus', 
    ('is_a', '$thing', 'jompus', True),
    ('is_a', '$thing', 'dumpus', True))

engine.add_rule('dumpus_is_bright', 
    ('is_a', '$thing', 'dumpus', True),
    ('is_bright', '$thing', True))

engine.add_rule('dumpus_is_numpus', 
    ('is_a', '$thing', 'dumpus', True),
    ('is_a', '$thing', 'numpus', True))

engine.add_rule('numpus_is_not_temperate', 
    ('is_a', '$thing', 'numpus', True),
    ('is_temperate', '$thing', False))

engine.add_rule('numpus_is_rompus', 
    ('is_a', '$thing', 'numpus', True),
    ('is_a', '$thing', 'rompus', True))

engine.add_rule('rompus_is_not_luminous', 
    ('is_a', '$thing', 'rompus', True),
    ('is_luminous', '$thing', False))

engine.add_rule('rompus_is_yumpus', 
    ('is_a', '$thing', 'rompus', True),
    ('is_a', '$thing', 'yumpus', True))

engine.add_rule('yumpus_is_opaque', 
    ('is_a', '$thing', 'yumpus', True),
    ('is_opaque', '$thing', True))

engine.add_rule('yumpus_is_impus', 
    ('is_a', '$thing', 'yumpus', True),
    ('is_a', '$thing', 'impus', True))

# Query section
engine.activate('bc_example')

result = engine.prove_1('facts', 'is_temperate', ('Stella', False), 1)
print("Stella is not temperate:", result is not None)