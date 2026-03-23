from pyke import knowledge_engine

# Create knowledge engine
engine = knowledge_engine.engine(__file__)

# Add facts using add_kb (knowledge base)
engine.add_kb('facts')
engine.add_fact('facts', 'is_a', ('Wren', 'vumpus', True))

# Rules for inheritance and properties
engine.add_rule('facts',
    ('tumpus_is_dull',
     (('is_a', '$thing', 'tumpus', True),),
     ('is_dull', '$thing', True)))

engine.add_rule('facts',
    ('tumpus_is_jompus',
     (('is_a', '$thing', 'tumpus', True),),
     ('is_a', '$thing', 'jompus', True)))

engine.add_rule('facts',
    ('jompus_is_not_sour',
     (('is_a', '$thing', 'jompus', True),),
     ('is_sour', '$thing', False)))

engine.add_rule('facts',
    ('jompus_is_vumpus',
     (('is_a', '$thing', 'jompus', True),),
     ('is_a', '$thing', 'vumpus', True)))

engine.add_rule('facts',
    ('vumpus_is_feisty',
     (('is_a', '$thing', 'vumpus', True),),
     ('is_feisty', '$thing', True)))

engine.add_rule('facts',
    ('vumpus_is_dumpus',
     (('is_a', '$thing', 'vumpus', True),),
     ('is_a', '$thing', 'dumpus', True)))

engine.add_rule('facts',
    ('dumpus_is_cold',
     (('is_a', '$thing', 'dumpus', True),),
     ('is_cold', '$thing', True)))

engine.add_rule('facts',
    ('dumpus_is_yumpus',
     (('is_a', '$thing', 'dumpus', True),),
     ('is_a', '$thing', 'yumpus', True)))

engine.add_rule('facts',
    ('yumpus_is_transparent',
     (('is_a', '$thing', 'yumpus', True),),
     ('is_transparent', '$thing', True)))

engine.add_rule('facts',
    ('yumpus_is_numpus',
     (('is_a', '$thing', 'yumpus', True),),
     ('is_a', '$thing', 'numpus', True)))

engine.add_rule('facts',
    ('numpus_is_not_amenable',
     (('is_a', '$thing', 'numpus', True),),
     ('is_amenable', '$thing', False)))

engine.add_rule('facts',
    ('numpus_is_zumpus',
     (('is_a', '$thing', 'numpus', True),),
     ('is_a', '$thing', 'zumpus', True)))

engine.add_rule('facts',
    ('zumpus_is_orange',
     (('is_a', '$thing', 'zumpus', True),),
     ('is_orange', '$thing', True)))

engine.add_rule('facts',
    ('zumpus_is_rompus',
     (('is_a', '$thing', 'zumpus', True),),
     ('is_a', '$thing', 'rompus', True)))

engine.add_rule('facts',
    ('rompus_is_earthy',
     (('is_a', '$thing', 'rompus', True),),
     ('is_earthy', '$thing', True)))

engine.add_rule('facts',
    ('impus_is_not_orange',
     (('is_a', '$thing', 'impus', True),),
     ('is_orange', '$thing', False)))

engine.add_rule('facts',
    ('rompus_is_wumpus',
     (('is_a', '$thing', 'rompus', True),),
     ('is_a', '$thing', 'wumpus', True)))

# Activate rules
engine.activate('facts')

# Query: Is Wren not orange? (i.e., is_orange(Wren, False))
result = engine.prove_1('facts', 'is_orange', ('Wren', False), 1)

# If result is None (cannot prove Wren is not orange), then the statement is false
# If result succeeds, then Wren is indeed not orange (statement true)
print("False" if result else "True")