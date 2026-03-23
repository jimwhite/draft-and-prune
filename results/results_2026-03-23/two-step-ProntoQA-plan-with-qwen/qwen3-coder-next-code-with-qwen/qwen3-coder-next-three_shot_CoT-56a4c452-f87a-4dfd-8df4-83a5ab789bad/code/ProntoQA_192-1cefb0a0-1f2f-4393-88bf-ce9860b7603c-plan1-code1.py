from pyke import knowledge_engine

# Initialize the knowledge engine
engine = knowledge_engine.engine(__file__)

# Add facts
engine.add_case_fact('facts', ('is_a', 'Sam', 'numpus', True))

# Add rules
engine.add_rule('rules',
    ('is_a', '?x', 'numpus', True),
    ('is_a', '?x', 'wumpus', True)
)

engine.add_rule('rules',
    ('is_a', '?x', 'wumpus', True),
    ('is_a', '?x', 'rompus', True)
)

engine.add_rule('rules',
    ('is_a', '?x', 'rompus', True),
    ('is_a', '?x', 'vumpus', True)
)

engine.add_rule('rules',
    ('is_a', '?x', 'vumpus', True),
    ('is_a', '?x', 'yumpus', True)
)

engine.add_rule('rules',
    ('is_a', '?x', 'yumpus', True),
    ('is_dull', '?x', True)
)

# Activate the rules
engine.activate('rules')

# Run inference
engine.run()

# Query: Is Sam not dull? (i.e., is_dull(Sam, False))
result = engine.query('facts', 'is_dull', ('Sam', False))

# Print result (None means false, a dict means true)
if result is None:
    print("False")
else:
    print("True")