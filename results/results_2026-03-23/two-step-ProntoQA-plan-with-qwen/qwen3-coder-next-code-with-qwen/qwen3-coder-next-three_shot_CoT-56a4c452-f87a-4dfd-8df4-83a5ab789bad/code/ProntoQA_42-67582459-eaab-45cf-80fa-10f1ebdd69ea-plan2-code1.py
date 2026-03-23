from pyke import knowledge_engine

engine = knowledge_engine.engine(__file__)

# Facts - explicitly stated facts
engine.add_kb_rule(
    'facts',
    'wren_is_vumpus',
    (),
    ('is_a', 'Wren', 'vumpus', True)
)

# Rules - encoding the logical implications
engine.add_kb_rule(
    'facts',
    'tumpus_is_jompus',
    (('is_a', '$thing', 'tumpus', True),),
    ('is_a', '$thing', 'jompus', True)
)

engine.add_kb_rule(
    'facts',
    'jompus_is_vumpus',
    (('is_a', '$thing', 'jompus', True),),
    ('is_a', '$thing', 'vumpus', True)
)

engine.add_kb_rule(
    'facts',
    'vumpus_is_dumpus',
    (('is_a', '$thing', 'vumpus', True),),
    ('is_a', '$thing', 'dumpus', True)
)

engine.add_kb_rule(
    'facts',
    'dumpus_is_yumpus',
    (('is_a', '$thing', 'dumpus', True),),
    ('is_a', '$thing', 'yumpus', True)
)

engine.add_kb_rule(
    'facts',
    'yumpus_is_numpus',
    (('is_a', '$thing', 'yumpus', True),),
    ('is_a', '$thing', 'numpus', True)
)

engine.add_kb_rule(
    'facts',
    'numpus_is_zumpus',
    (('is_a', '$thing', 'numpus', True),),
    ('is_a', '$thing', 'zumpus', True)
)

engine.add_kb_rule(
    'facts',
    'zumpus_is_orange',
    (('is_a', '$thing', 'zumpus', True),),
    ('is_orange', '$thing', True)
)

engine.add_kb_rule(
    'facts',
    'rompus_is_wumpus',
    (('is_a', '$thing', 'rompus', True),),
    ('is_a', '$thing', 'wumpus', True)
)

# Additional rules for completeness (though not needed for this query)
engine.add_kb_rule(
    'facts',
    'vumpus_is_feisty',
    (('is_a', '$thing', 'vumpus', True),),
    ('is_feisty', '$thing', True)
)

engine.add_kb_rule(
    'facts',
    'dumpus_is_cold',
    (('is_a', '$thing', 'dumpus', True),),
    ('is_cold', '$thing', True)
)

engine.add_kb_rule(
    'facts',
    'yumpus_is_transparent',
    (('is_a', '$thing', 'yumpus', True),),
    ('is_transparent', '$thing', True)
)

engine.add_kb_rule(
    'facts',
    'numpus_is_not_amenable',
    (('is_a', '$thing', 'numpus', True),),
    ('is_amenable', '$thing', False)
)

engine.add_kb_rule(
    'facts',
    'zumpus_is_rompus',
    (('is_a', '$thing', 'zumpus', True),),
    ('is_a', '$thing', 'rompus', True)
)

engine.add_kb_rule(
    'facts',
    'rompus_is_earthy',
    (('is_a', '$thing', 'rompus', True),),
    ('is_earthy', '$thing', True)
)

engine.add_kb_rule(
    'facts',
    'impus_is_not_orange',
    (('is_a', '$thing', 'impus', True),),
    ('is_orange', '$thing', False)
)

# Query: Is Wren not orange? (i.e., is_orange('Wren', False))
# We want to check if we can prove that Wren is NOT orange
query = engine.prove_1('facts', 'is_orange', ('Wren', False))

print("Query result:", query)