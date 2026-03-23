from pyke import knowledge_engine

# Create knowledge engine instance
engine = knowledge_engine.engine(__file__)

# Add facts
engine.add_case_fact('facts', ('is_a', 'Sam', 'numpus', True))

# Add rules
engine.add_rule('rules',
    ('is_a', '$X', 'numpus', True),
    ('is_a', '$X', 'wumpus', True)
)

engine.add_rule('rules',
    ('is_a', '$X', 'wumpus', True),
    ('is_a', '$X', 'rompus', True)
)

engine.add_rule('rules',
    ('is_a', '$X', 'rompus', True),
    ('is_a', '$X', 'vumpus', True)
)

engine.add_rule('rules',
    ('is_a', '$X', 'vumpus', True),
    ('is_a', '$X', 'yumpus', True)
)

engine.add_rule('rules',
    ('is_a', '$X', 'yumpus', True),
    ('is_dull', '$X', True)
)

# Activate rules
engine.activate('rules')

# Run inference
engine.run()

# Query: Is Sam not dull? (i.e., is_dull(Sam, False))
result = engine.query('facts', 'is_dull', ('Sam', False))

# Print result (None means false, non-None means true)
if result is None:
    print("False")
else:
    print("True")