from pyke import knowledge_engine, fact_base

# Create knowledge engine instance
engine = knowledge_engine.engine(__file__)

# Define facts
engine.add_case_fact('facts', ('is_blue', 'bear', True))
engine.add_case_fact('facts', ('is_green', 'bear', True))
engine.add_case_fact('facts', ('is_red', 'bear', True))
engine.add_case_fact('facts', ('sees', 'bear', 'rabbit', True))

engine.add_case_fact('facts', ('is_blue', 'cow', True))
engine.add_case_fact('facts', ('needs', 'cow', 'tiger', True))
engine.add_case_fact('facts', ('visits', 'cow', 'rabbit', True))

engine.add_case_fact('facts', ('is_cold', 'rabbit', True))
engine.add_case_fact('facts', ('is_nice', 'rabbit', True))
engine.add_case_fact('facts', ('needs', 'rabbit', 'cow', True))
engine.add_case_fact('facts', ('sees', 'rabbit', 'cow', True))
engine.add_case_fact('facts', ('sees', 'rabbit', 'tiger', True))

engine.add_case_fact('facts', ('needs', 'tiger', 'bear', True))
engine.add_case_fact('facts', ('needs', 'tiger', 'rabbit', True))
engine.add_case_fact('facts', ('visits', 'tiger', 'bear', True))
engine.add_case_fact('facts', ('visits', 'tiger', 'cow', True))

# Define rules
engine.add_rule('rules', 
    ('is_green', '?x', True),
    ('visits', '?x', 'tiger', True))

engine.add_rule('rules',
    ('sees', '?x', 'bear', True),
    ('is_cold', '?x', True),
    ('is_green', 'bear', True))

engine.add_rule('rules',
    ('needs', 'cow', 'rabbit', True),
    ('needs', 'rabbit', 'cow', True),
    ('is_red', 'rabbit', True))

engine.add_rule('rules',
    ('is_green', '?x', True),
    ('needs', '?x', 'cow', True))

engine.add_rule('rules',
    ('visits', '?x', 'tiger', True),
    ('is_red', 'tiger', True))

engine.add_rule('rules',
    ('needs', '?x', 'tiger', True),
    ('sees', 'tiger', 'cow', True),
    ('needs', 'cow', 'bear', True))

engine.add_rule('rules',
    ('sees', '?x', 'bear', True),
    ('needs', '?x', 'bear', True),
    ('sees', '?x', 'cow', True))

engine.add_rule('rules',
    ('visits', '?x', 'rabbit', True),
    ('needs', 'rabbit', 'tiger', True))

engine.add_rule('rules',
    ('needs', '?x', 'bear', True),
    ('visits', 'bear', 'tiger', True),
    ('sees', '?x', 'bear', True))

# Run the engine to infer new facts
engine.activate('rules')

# Query: does the cow visit the rabbit?
result = engine.query(('visits', 'cow', 'rabbit', True))

print("True" if result else "False")