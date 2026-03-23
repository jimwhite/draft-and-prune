from pyke import knowledge_engine

# Create engine instance
engine = knowledge_engine.engine(__file__)

# Add facts and rules
engine.add_case_fact('facts', ('is_a', 'Polly', 'vumpus', True))

# Rules
engine.add_rule(
    # Rule: Every vumpus is transparent.
    'vumpus_is_transparent',
    [('facts', 'is_a', '$thing', 'vumpus', True)],
    [('facts', 'is_transparent', '$thing', True)]
)

engine.add_rule(
    # Rule: Vumpuses are zumpuses.
    'vumpus_is_zumpus',
    [('facts', 'is_a', '$thing', 'vumpus', True)],
    [('facts', 'is_a', '$thing', 'zumpus', True)]
)

engine.add_rule(
    # Rule: Every zumpus is not large.
    'zumpus_is_not_large',
    [('facts', 'is_a', '$thing', 'zumpus', True)],
    [('facts', 'is_large', '$thing', False)]
)

engine.add_rule(
    # Rule: Zumpuses are dumpuses.
    'zumpus_is_dumpus',
    [('facts', 'is_a', '$thing', 'zumpus', True)],
    [('facts', 'is_a', '$thing', 'dumpus', True)]
)

engine.add_rule(
    # Rule: Every dumpus is spicy.
    'dumpus_is_spicy',
    [('facts', 'is_a', '$thing', 'dumpus', True)],
    [('facts', 'is_spicy', '$thing', True)]
)

engine.add_rule(
    # Rule: Each dumpus is a numpus.
    'dumpus_is_numpus',
    [('facts', 'is_a', '$thing', 'dumpus', True)],
    [('facts', 'is_a', '$thing', 'numpus', True)]
)

engine.add_rule(
    # Rule: Each impus is blue.
    'impus_is_blue',
    [('facts', 'is_a', '$thing', 'impus', True)],
    [('facts', 'is_blue', '$thing', True)]
)

engine.add_rule(
    # Rule: Numpuses are temperate.
    'numpus_is_temperate',
    [('facts', 'is_a', '$thing', 'numpus', True)],
    [('facts', 'is_temperate', '$thing', True)]
)

engine.add_rule(
    # Rule: Every numpus is a tumpus.
    'numpus_is_tumpus',
    [('facts', 'is_a', '$thing', 'numpus', True)],
    [('facts', 'is_a', '$thing', 'tumpus', True)]
)

engine.add_rule(
    # Rule: Tumpuses are not blue.
    'tumpus_is_not_blue',
    [('facts', 'is_a', '$thing', 'tumpus', True)],
    [('facts', 'is_blue', '$thing', False)]
)

engine.add_rule(
    # Rule: Tumpuses are jompuses.
    'tumpus_is_jompus',
    [('facts', 'is_a', '$thing', 'tumpus', True)],
    [('facts', 'is_a', '$thing', 'jompus', True)]
)

engine.add_rule(
    # Rule: Each jompus is happy.
    'jompus_is_happy',
    [('facts', 'is_a', '$thing', 'jompus', True)],
    [('facts', 'is_happy', '$thing', True)]
)

engine.add_rule(
    # Rule: Each jompus is a yumpus.
    'jompus_is_yumpus',
    [('facts', 'is_a', '$thing', 'jompus', True)],
    [('facts', 'is_a', '$thing', 'yumpus', True)]
)

engine.add_rule(
    # Rule: Each yumpus is not amenable.
    'yumpus_is_not_amenable',
    [('facts', 'is_a', '$thing', 'yumpus', True)],
    [('facts', 'is_amenable', '$thing', False)]
)

engine.add_rule(
    # Rule: Every yumpus is a wumpus.
    'yumpus_is_wumpus',
    [('facts', 'is_a', '$thing', 'yumpus', True)],
    [('facts', 'is_a', '$thing', 'wumpus', True)]
)

engine.add_rule(
    # Rule: Wumpuses are not floral.
    'wumpus_is_not_floral',
    [('facts', 'is_a', '$thing', 'wumpus', True)],
    [('facts', 'is_floral', '$thing', False)]
)

engine.add_rule(
    # Rule: Wumpuses are rompuses.
    'wumpus_is_rompus',
    [('facts', 'is_a', '$thing', 'wumpus', True)],
    [('facts', 'is_a', '$thing', 'rompus', True)]
)

# Activate the knowledge base
engine.activate('rules')

# Query: Is Polly not blue?
result = engine.prove_1('facts', 'is_blue', ('Polly', False), 1)

print("Statement: Polly is not blue.")
if result:
    print("True")
else:
    print("False")