# Import required modules
from pyke import knowledge_engine

# Initialize the knowledge engine
engine = knowledge_engine.engine(__file__)

# Facts
facts_kb = engine.add_kb('facts')
facts_kb.add(('is_a', 'Rex', 'yumpus', True))

# Rules
rules_kb = engine.add_kb('rules')

# Rule: Each impus is a yumpus.
rules_kb.add((
    'impus_is_yumpus',
    ('is_a', '$thing', 'impus', True),
    ('is_a', '$thing', 'yumpus', True)
))

# Rule: Yumpuses are blue.
rules_kb.add((
    'yumpus_is_blue',
    ('is_a', '$thing', 'yumpus', True),
    ('is_blue', '$thing', True)
))

# Rule: Yumpuses are wumpuses.
rules_kb.add((
    'yumpus_is_wumpus',
    ('is_a', '$thing', 'yumpus', True),
    ('is_a', '$thing', 'wumpus', True)
))

# Rule: Wumpuses are hot.
rules_kb.add((
    'wumpus_is_hot',
    ('is_a', '$thing', 'wumpus', True),
    ('is_hot', '$thing', True)
))

# Rule: Every wumpus is a numpus.
rules_kb.add((
    'wumpus_is_numpus',
    ('is_a', '$thing', 'wumpus', True),
    ('is_a', '$thing', 'numpus', True)
))

# Rule: Jompuses are happy.
rules_kb.add((
    'jompus_is_happy',
    ('is_a', '$thing', 'jompus', True),
    ('is_happy', '$thing', True)
))

# Rule: Numpuses are fruity.
rules_kb.add((
    'numpus_is_fruity',
    ('is_a', '$thing', 'numpus', True),
    ('is_fruity', '$thing', True)
))

# Rule: Numpuses are dumpuses.
rules_kb.add((
    'numpus_is_dumpus',
    ('is_a', '$thing', 'numpus', True),
    ('is_a', '$thing', 'dumpus', True)
))

# Rule: Every dumpus is not dull.
rules_kb.add((
    'dumpus_is_not_dull',
    ('is_a', '$thing', 'dumpus', True),
    ('is_dull', '$thing', False)
))

# Rule: Every dumpus is a tumpus.
rules_kb.add((
    'dumpus_is_tumpus',
    ('is_a', '$thing', 'dumpus', True),
    ('is_a', '$thing', 'tumpus', True)
))

# Rule: Tumpuses are not happy.
rules_kb.add((
    'tumpus_is_not_happy',
    ('is_a', '$thing', 'tumpus', True),
    ('is_happy', '$thing', False)
))

# Rule: Every tumpus is a vumpus.
rules_kb.add((
    'tumpus_is_vumpus',
    ('is_a', '$thing', 'tumpus', True),
    ('is_a', '$thing', 'vumpus', True)
))

# Rule: Vumpuses are not opaque.
rules_kb.add((
    'vumpus_is_not_opaque',
    ('is_a', '$thing', 'vumpus', True),
    ('is_opaque', '$thing', False)
))

# Rule: Every vumpus is a rompus.
rules_kb.add((
    'vumpus_is_rompus',
    ('is_a', '$thing', 'vumpus', True),
    ('is_a', '$thing', 'rompus', True)
))

# Rule: Rompuses are metallic.
rules_kb.add((
    'rompus_is_metallic',
    ('is_a', '$thing', 'rompus', True),
    ('is_metallic', '$thing', True)
))

# Rule: Each rompus is a zumpus.
rules_kb.add((
    'rompus_is_zumpus',
    ('is_a', '$thing', 'rompus', True),
    ('is_a', '$thing', 'zumpus', True)
))

# Query - Check if "Rex is not happy" is true
query_kb = engine.add_kb('query')
# We want to prove that Rex is not happy, so we query for is_happy(Rex, False)
# In PyKe, we can use the prove method to check if this goal can be satisfied
query_kb.add(('is_happy', 'Rex', False))