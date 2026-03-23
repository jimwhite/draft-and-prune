from pyke import knowledge_engine, goal

# Create knowledge engine instance
engine = knowledge_engine.engine(__file__)

# Define facts
engine.add_case_fact('kb', ('is_big', 'Bob', True))
engine.add_case_fact('kb', ('is_blue', 'Bob', True))
engine.add_case_fact('kb', ('is_cold', 'Bob', True))
engine.add_case_fact('kb', ('is_quiet', 'Bob', True))
engine.add_case_fact('kb', ('is_rough', 'Bob', True))
engine.add_case_fact('kb', ('is_smart', 'Bob', True))
engine.add_case_fact('kb', ('is_white', 'Bob', True))

engine.add_case_fact('kb', ('is_rough', 'Dave', True))
engine.add_case_fact('kb', ('is_blue', 'Fiona', True))
engine.add_case_fact('kb', ('is_big', 'Harry', True))
engine.add_case_fact('kb', ('is_cold', 'Harry', True))

# Define rules
engine.add_rule('kb', 
    ('is_blue', '?x', True),
    ('is_cold', '?x', True))

engine.add_rule('kb',
    ('is_big', '?x', True),
    ('is_white', '?x', True))

engine.add_rule('kb',
    (('is_blue', '?x', True), ('is_smart', '?x', True)),
    ('is_big', '?x', True))

engine.add_rule('kb',
    (('is_blue', '?x', True), ('is_rough', '?x', True)),
    ('is_quiet', '?x', True))

engine.add_rule('kb',
    ('is_smart', '?x', True),
    ('is_blue', '?x', True))

engine.add_rule('kb',
    ('is_cold', '?x', True),
    ('is_rough', '?x', True))

engine.add_rule('kb',
    ('is_quiet', '?x', True),
    ('is_big', '?x', True))

# Add query
engine.add_goal('kb', ('is_big', 'Fiona', True))

# Run the engine
engine.activate('kb')

# Check result
result = engine.prove('kb', ('is_big', 'Fiona', True), 1)
print(result is not None)