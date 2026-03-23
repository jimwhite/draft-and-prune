from pyke import knowledge_engine, facts, rules

# Initialize the knowledge engine
engine = knowledge_engine.engine(__name__)

# Facts
engine.add_universal_fact('is_a', 'Stella', 'numpus', True)

# Rules
engine.add_universal_rule(
    'zumpus_is_metallic',
    ('is_a', '$thing', 'zumpus', True),
    ('is_metallic', '$thing', True)
)

engine.add_universal_rule(
    'zumpus_is_wumpus',
    ('is_a', '$thing', 'zumpus', True),
    ('is_a', '$thing', 'wumpus', True)
)

engine.add_universal_rule(
    'wumpus_is_not_floral',
    ('is_a', '$thing', 'wumpus', True),
    ('is_floral', '$thing', False)
)

engine.add_universal_rule(
    'wumpus_is_numpus',
    ('is_a', '$thing', 'wumpus', True),
    ('is_a', '$thing', 'numpus', True)
)

engine.add_universal_rule(
    'numpus_is_happy',
    ('is_a', '$thing', 'numpus', True),
    ('is_happy', '$thing', True)
)

engine.add_universal_rule(
    'numpus_is_impus',
    ('is_a', '$thing', 'numpus', True),
    ('is_a', '$thing', 'impus', True)
)

engine.add_universal_rule(
    'impus_is_kind',
    ('is_a', '$thing', 'impus', True),
    ('is_kind', '$thing', True)
)

engine.add_universal_rule(
    'impus_is_rompus',
    ('is_a', '$thing', 'impus', True),
    ('is_a', '$thing', 'rompus', True)
)

engine.add_universal_rule(
    'rompus_is_large',
    ('is_a', '$thing', 'rompus', True),
    ('is_large', '$thing', True)
)

engine.add_universal_rule(
    'vumpus_is_opaque',
    ('is_a', '$thing', 'vumpus', True),
    ('is_opaque', '$thing', True)
)

engine.add_universal_rule(
    'rompus_is_jompus',
    ('is_a', '$thing', 'rompus', True),
    ('is_a', '$thing', 'jompus', True)
)

engine.add_universal_rule(
    'jompus_is_cold',
    ('is_a', '$thing', 'jompus', True),
    ('is_cold', '$thing', True)
)

engine.add_universal_rule(
    'jompus_is_dumpus',
    ('is_a', '$thing', 'jompus', True),
    ('is_a', '$thing', 'dumpus', True)
)

engine.add_universal_rule(
    'dumpus_is_not_opaque',
    ('is_a', '$thing', 'dumpus', True),
    ('is_opaque', '$thing', False)
)

engine.add_universal_rule(
    'dumpus_is_yumpus',
    ('is_a', '$thing', 'dumpus', True),
    ('is_a', '$thing', 'yumpus', True)
)

engine.add_universal_rule(
    'yumpus_is_spicy',
    ('is_a', '$thing', 'yumpus', True),
    ('is_spicy', '$thing', True)
)

engine.add_universal_rule(
    'yumpus_is_tumpus',
    ('is_a', '$thing', 'yumpus', True),
    ('is_a', '$thing', 'tumpus', True)
)

# Activate the knowledge base
engine.activate('bc_example')

# Query: Is Stella opaque?
result = engine.query(('is_opaque', 'Stella', True))

# Output the result
print("False" if not result else "True")