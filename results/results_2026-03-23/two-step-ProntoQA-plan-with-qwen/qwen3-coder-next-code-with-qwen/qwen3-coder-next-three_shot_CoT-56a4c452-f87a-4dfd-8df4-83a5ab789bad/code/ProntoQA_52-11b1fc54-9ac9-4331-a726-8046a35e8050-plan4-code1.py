from pyke import knowledge_engine, goal

# Create and initialize the knowledge engine
engine = knowledge_engine.engine(__file__)

# Define facts and rules programmatically
# First, we need to define the knowledge base structure
engine.add_assertion('facts', 'is_a', 'Polly', 'jompus', True)

# Add rules using PyKe's rule syntax
engine.add_rule('jompus_is_spicy', 
    ('facts', 'is_a', '$thing', 'jompus', True),
    ('facts', 'is_spicy', '$thing', True))

engine.add_rule('jompus_is_dumpus',
    ('facts', 'is_a', '$thing', 'jompus', True),
    ('facts', 'is_a', '$thing', 'dumpus', True))

engine.add_rule('dumpus_is_not_transparent',
    ('facts', 'is_a', '$thing', 'dumpus', True),
    ('facts', 'is_transparent', '$thing', False))

engine.add_rule('dumpus_is_zumpus',
    ('facts', 'is_a', '$thing', 'dumpus', True),
    ('facts', 'is_a', '$thing', 'zumpus', True))

engine.add_rule('zumpus_is_feisty',
    ('facts', 'is_a', '$thing', 'zumpus', True),
    ('facts', 'is_feisty', '$thing', True))

engine.add_rule('zumpus_is_wumpus',
    ('facts', 'is_a', '$thing', 'zumpus', True),
    ('facts', 'is_a', '$thing', 'wumpus', True))

engine.add_rule('wumpus_is_not_dull',
    ('facts', 'is_a', '$thing', 'wumpus', True),
    ('facts', 'is_dull', '$thing', False))

engine.add_rule('wumpus_is_impus',
    ('facts', 'is_a', '$thing', 'wumpus', True),
    ('facts', 'is_a', '$thing', 'impus', True))

engine.add_rule('vumpus_is_not_blue',
    ('facts', 'is_a', '$thing', 'vumpus', True),
    ('facts', 'is_blue', '$thing', False))

engine.add_rule('impus_is_blue',
    ('facts', 'is_a', '$thing', 'impus', True),
    ('facts', 'is_blue', '$thing', True))

engine.add_rule('impus_is_tumpus',
    ('facts', 'is_a', '$thing', 'impus', True),
    ('facts', 'is_a', '$thing', 'tumpus', True))

engine.add_rule('tumpus_is_not_floral',
    ('facts', 'is_a', '$thing', 'tumpus', True),
    ('facts', 'is_floral', '$thing', False))

engine.add_rule('tumpus_is_numpus',
    ('facts', 'is_a', '$thing', 'tumpus', True),
    ('facts', 'is_a', '$thing', 'numpus', True))

# Run the engine to apply all rules
engine.run()

# Query: Is Polly blue?
result = engine.query(('facts', 'is_blue', 'Polly', True))
print(result)