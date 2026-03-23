from pyke import knowledge_engine

# Initialize knowledge engine
engine = knowledge_engine.engine(__file__)

# Facts
engine.add_case_fact('facts', ('is_a', 'Max', 'numpus', True))

# Rules
engine.add_rule(
    'rompus_is_not_large',
    ('is_a', '$thing', 'rompus', True),
    ('is_large', '$thing', False)
)

engine.add_rule(
    'rompus_is_numpus',
    ('is_a', '$thing', 'rompus', True),
    ('is_a', '$thing', 'numpus', True)
)

engine.add_rule(
    'numpus_is_fruity',
    ('is_a', '$thing', 'numpus', True),
    ('is_fruity', '$thing', True)
)

engine.add_rule(
    'numpus_is_wumpus',
    ('is_a', '$thing', 'numpus', True),
    ('is_a', '$thing', 'wumpus', True)
)

engine.add_rule(
    'wumpus_is_not_metallic',
    ('is_a', '$thing', 'wumpus', True),
    ('is_metallic', '$thing', False)
)

engine.add_rule(
    'wumpus_is_tumpus',
    ('is_a', '$thing', 'wumpus', True),
    ('is_a', '$thing', 'tumpus', True)
)

engine.add_rule(
    'tumpus_is_cold',
    ('is_a', '$thing', 'tumpus', True),
    ('is_cold', '$thing', True)
)

engine.add_rule(
    'dumpus_is_not_brown',
    ('is_a', '$thing', 'dumpus', True),
    ('is_brown', '$thing', False)
)

engine.add_rule(
    'tumpus_is_jompus',
    ('is_a', '$thing', 'tumpus', True),
    ('is_a', '$thing', 'jompus', True)
)

engine.add_rule(
    'jompus_is_sweet',
    ('is_a', '$thing', 'jompus', True),
    ('is_sweet', '$thing', True)
)

engine.add_rule(
    'jompus_is_zumpus',
    ('is_a', '$thing', 'jompus', True),
    ('is_a', '$thing', 'zumpus', True)
)

engine.add_rule(
    'zumpus_is_brown',
    ('is_a', '$thing', 'zumpus', True),
    ('is_brown', '$thing', True)
)

engine.add_rule(
    'zumpus_is_yumpus',
    ('is_a', '$thing', 'zumpus', True),
    ('is_a', '$thing', 'yumpus', True)
)

# Query: Is Max not brown?
result = engine.prove_1('facts', 'is_brown', ('Max', False), 1)
print("False" if result else "True")