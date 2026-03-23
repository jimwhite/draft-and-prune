from pyke import knowledge_engine

# Create knowledge engine instance
engine = knowledge_engine.Engine(__name__)

# Define the knowledge base
engine.add_rule('facts', 'numpus_is_vumpus',
    ('is_a', '$x', 'numpus'),
    ('is_a', '$x', 'vumpus'))

engine.add_rule('facts', 'numpus_is_earthy',
    ('is_a', '$x', 'numpus'),
    ('is_earthy', '$x'))

engine.add_rule('facts', 'vumpus_is_transparent',
    ('is_a', '$x', 'vumpus'),
    ('is_transparent', '$x'))

engine.add_rule('facts', 'vumpus_is_tumpus',
    ('is_a', '$x', 'vumpus'),
    ('is_a', '$x', 'tumpus'))

engine.add_rule('facts', 'tumpus_is_small',
    ('is_a', '$x', 'tumpus'),
    ('is_small', '$x'))

engine.add_rule('facts', 'tumpus_is_dumpus',
    ('is_a', '$x', 'tumpus'),
    ('is_a', '$x', 'dumpus'))

engine.add_rule('facts', 'dumpus_is_not_aggressive',
    ('is_a', '$x', 'dumpus'),
    ('not_aggressive', '$x'))

engine.add_rule('facts', 'dumpus_is_wumpus',
    ('is_a', '$x', 'dumpus'),
    ('is_a', '$x', 'wumpus'))

engine.add_rule('facts', 'wumpus_is_not_wooden',
    ('is_a', '$x', 'wumpus'),
    ('not_wooden', '$x'))

engine.add_rule('facts', 'wumpus_is_jompus',
    ('is_a', '$x', 'wumpus'),
    ('is_a', '$x', 'jompus'))

engine.add_rule('facts', 'jompus_is_not_nervous',
    ('is_a', '$x', 'jompus'),
    ('not_nervous', '$x'))

engine.add_rule('facts', 'jompus_is_zumpus',
    ('is_a', '$x', 'jompus'),
    ('is_a', '$x', 'zumpus'))

engine.add_rule('facts', 'zumpus_is_temperate',
    ('is_a', '$x', 'zumpus'),
    ('is_temperate', '$x'))

engine.add_rule('facts', 'rompus_is_wooden',
    ('is_a', '$x', 'rompus'),
    ('is_wooden', '$x'))

engine.add_rule('facts', 'zumpus_is_impus',
    ('is_a', '$x', 'zumpus'),
    ('is_a', '$x', 'impus'))

engine.add_rule('facts', 'impus_is_blue',
    ('is_a', '$x', 'impus'),
    ('is_blue', '$x'))

engine.add_rule('facts', 'impus_is_yumpus',
    ('is_a', '$x', 'impus'),
    ('is_a', '$x', 'yumpus'))

# Add facts
engine.add_assertion('facts', ('is_a', 'Sally', 'numpus'))

# Run the engine
engine.activate('facts')

# Query: Is Sally not wooden?
result = engine.query(('facts', 'not_wooden', 'Sally'))
print(result)