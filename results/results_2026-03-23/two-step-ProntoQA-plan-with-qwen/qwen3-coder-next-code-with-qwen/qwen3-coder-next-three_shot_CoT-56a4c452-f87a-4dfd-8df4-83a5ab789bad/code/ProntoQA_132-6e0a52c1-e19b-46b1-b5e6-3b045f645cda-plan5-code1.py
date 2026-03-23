# Import required modules
from pyke import knowledge_engine

# Initialize knowledge engine
engine = knowledge_engine.engine(__file__)

# Facts
engine.add_case_fact('facts', ('is_a', 'Polly', 'vumpus', True))

# Rules
engine.add_rule('vumpus_is_transparent', 
    ('facts', 'is_a', '$thing', 'vumpus', True),
    [('facts', 'has_prop', '$thing', 'transparent', True)])

engine.add_rule('vumpus_is_zumpus',
    ('facts', 'is_a', '$thing', 'vumpus', True),
    [('facts', 'is_a', '$thing', 'zumpus', True)])

engine.add_rule('zumpus_is_not_large',
    ('facts', 'is_a', '$thing', 'zumpus', True),
    [('facts', 'has_prop', '$thing', 'large', False)])

engine.add_rule('zumpus_is_dumpus',
    ('facts', 'is_a', '$thing', 'zumpus', True),
    [('facts', 'is_a', '$thing', 'dumpus', True)])

engine.add_rule('dumpus_is_spicy',
    ('facts', 'is_a', '$thing', 'dumpus', True),
    [('facts', 'has_prop', '$thing', 'spicy', True)])

engine.add_rule('dumpus_is_numpus',
    ('facts', 'is_a', '$thing', 'dumpus', True),
    [('facts', 'is_a', '$thing', 'numpus', True)])

engine.add_rule('impus_is_blue',
    ('facts', 'is_a', '$thing', 'impus', True),
    [('facts', 'has_prop', '$thing', 'blue', True)])

engine.add_rule('numpus_is_temperate',
    ('facts', 'is_a', '$thing', 'numpus', True),
    [('facts', 'has_prop', '$thing', 'temperate', True)])

engine.add_rule('numpus_is_tumpus',
    ('facts', 'is_a', '$thing', 'numpus', True),
    [('facts', 'is_a', '$thing', 'tumpus', True)])

engine.add_rule('tumpus_is_not_blue',
    ('facts', 'is_a', '$thing', 'tumpus', True),
    [('facts', 'has_prop', '$thing', 'blue', False)])

engine.add_rule('tumpus_is_jompus',
    ('facts', 'is_a', '$thing', 'tumpus', True),
    [('facts', 'is_a', '$thing', 'jompus', True)])

engine.add_rule('jompus_is_happy',
    ('facts', 'is_a', '$thing', 'jompus', True),
    [('facts', 'has_prop', '$thing', 'happy', True)])

engine.add_rule('jompus_is_yumpus',
    ('facts', 'is_a', '$thing', 'jompus', True),
    [('facts', 'is_a', '$thing', 'yumpus', True)])

engine.add_rule('yumpus_is_not_amenable',
    ('facts', 'is_a', '$thing', 'yumpus', True),
    [('facts', 'has_prop', '$thing', 'amenable', False)])

engine.add_rule('yumpus_is_wumpus',
    ('facts', 'is_a', '$thing', 'yumpus', True),
    [('facts', 'is_a', '$thing', 'wumpus', True)])

engine.add_rule('wumpus_is_not_floral',
    ('facts', 'is_a', '$thing', 'wumpus', True),
    [('facts', 'has_prop', '$thing', 'floral', False)])

engine.add_rule('wumpus_is_rompus',
    ('facts', 'is_a', '$thing', 'wumpus', True),
    [('facts', 'is_a', '$thing', 'rompus', True)])

# Build the knowledge base
engine.build()

# Query: Is Polly not blue?
result = engine.query().facts.has_prop('Polly', 'blue', False)

# Output the result
print("True" if result else "False")