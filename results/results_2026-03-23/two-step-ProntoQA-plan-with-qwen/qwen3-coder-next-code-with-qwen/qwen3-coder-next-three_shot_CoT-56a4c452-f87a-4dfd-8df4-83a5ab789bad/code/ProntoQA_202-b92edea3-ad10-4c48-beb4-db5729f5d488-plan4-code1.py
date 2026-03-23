from pyke import knowledge_engine

engine = knowledge_engine.engine(__file__)

# Facts
engine.add_case_fact('facts', ('is_a', 'Wren', 'zumpus', True))

# Rules
engine.add_rule('rules',
    ('is_a', '?x', 'zumpus', True),
    ('is_a', '?x', 'rompus', True)
)

engine.add_rule('rules',
    ('is_a', '?x', 'rompus', True),
    ('is_a', '?x', 'dumpus', True)
)

engine.add_rule('rules',
    ('is_a', '?x', 'dumpus', True),
    ('is_a', '?x', 'wumpus', True)
)

engine.add_rule('rules',
    ('is_a', '?x', 'wumpus', True),
    ('is_a', '?x', 'vumpus', True)
)

engine.add_rule('rules',
    ('is_a', '?x', 'vumpus', True),
    ('not_opaque', '?x', True)
)

# Query
result = engine.prove_1_goal('facts.is_opaque("Wren", True)')
print(result is None)  # If result is None, the goal cannot be proven (i.e., Wren is NOT opaque)