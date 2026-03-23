from pyke import knowledge_engine

engine = knowledge_engine.engine(__file__)

# Facts
engine.add_rule('facts', 'is_a', ('Rex', 'zumpus', True))

# Rules
engine.add_rule('rules', 'zumpus_is_not_temperate',
    (('facts', 'is_a', '$thing', 'zumpus', True),),
    ('facts', 'is_temperate', ('$thing', False)))

engine.add_rule('rules', 'zumpus_is_vumpus',
    (('facts', 'is_a', '$thing', 'zumpus', True),),
    ('facts', 'is_a', ('$thing', 'vumpus', True)))

engine.add_rule('rules', 'vumpus_is_large',
    (('facts', 'is_a', '$thing', 'vumpus', True),),
    ('facts', 'is_large', ('$thing', True)))

engine.add_rule('rules', 'vumpus_is_dumpus',
    (('facts', 'is_a', '$thing', 'vumpus', True),),
    ('facts', 'is_a', ('$thing', 'dumpus', True)))

engine.add_rule('rules', 'dumpus_is_feisty',
    (('facts', 'is_a', '$thing', 'dumpus', True),),
    ('facts', 'is_feisty', ('$thing', True)))

engine.add_rule('rules', 'tumpus_is_not_opaque',
    (('facts', 'is_a', '$thing', 'tumpus', True),),
    ('facts', 'is_opaque', ('$thing', False)))

engine.add_rule('rules', 'dumpus_is_wumpus',
    (('facts', 'is_a', '$thing', 'dumpus', True),),
    ('facts', 'is_a', ('$thing', 'wumpus', True)))

engine.add_rule('rules', 'wumpus_is_floral',
    (('facts', 'is_a', '$thing', 'wumpus', True),),
    ('facts', 'is_floral', ('$thing', True)))

engine.add_rule('rules', 'wumpus_is_rompus',
    (('facts', 'is_a', '$thing', 'wumpus', True),),
    ('facts', 'is_a', ('$thing', 'rompus', True)))

engine.add_rule('rules', 'rompus_is_opaque',
    (('facts', 'is_a', '$thing', 'rompus', True),),
    ('facts', 'is_opaque', ('$thing', True)))

engine.add_rule('rules', 'rompus_is_numpus',
    (('facts', 'is_a', '$thing', 'rompus', True),),
    ('facts', 'is_a', ('$thing', 'numpus', True)))

# Query: Is Rex not opaque? (i.e., is_opaque(Rex, False))
engine.add_query('query', 'is_opaque', ('Rex', False))

# Run the engine and get results
engine.activate('rules')
result = list(engine.prove_goal('query'))
is_true = len(result) > 0

print("Rex is not opaque:", is_true)