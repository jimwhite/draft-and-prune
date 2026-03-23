from pyke import knowledge_engine

# Create and initialize the knowledge engine
engine = knowledge_engine.engine(__file__)
engine.activate('rules')

# Facts section
engine.add_case_fact('facts', ('is_a', 'Sam', 'numpus', True))
engine.add_case_fact('facts', ('is_a', 'numpus', 'wumpus', True))
engine.add_case_fact('facts', ('is_wooden', 'numpus', False))
engine.add_case_fact('facts', ('is_small', 'wumpus', True))
engine.add_case_fact('facts', ('is_a', 'wumpus', 'rompus', True))
engine.add_case_fact('facts', ('is_floral', 'rompus', False))
engine.add_case_fact('facts', ('is_a', 'rompus', 'vumpus', True))
engine.add_case_fact('facts', ('is_blue', 'vumpus', True))
engine.add_case_fact('facts', ('is_a', 'vumpus', 'yumpus', True))
engine.add_case_fact('facts', ('is_dull', 'yumpus', True))
engine.add_case_fact('facts', ('is_a', 'yumpus', 'zumpus', True))
engine.add_case_fact('facts', ('is_dull', 'jompus', False))

# Rules section
engine.add_rule('rules',
    ('is_a(?x, ?y)', 'is_a(?y, ?z)'),
    ('is_a', '?x', '?z')
)

# Query section
result = engine.ask1('facts.is_dull("Sam", True)')
print(result)