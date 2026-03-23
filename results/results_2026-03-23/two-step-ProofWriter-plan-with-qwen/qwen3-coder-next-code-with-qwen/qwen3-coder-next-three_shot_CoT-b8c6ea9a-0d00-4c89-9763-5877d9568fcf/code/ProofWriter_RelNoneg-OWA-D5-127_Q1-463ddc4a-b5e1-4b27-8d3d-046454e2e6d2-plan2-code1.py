from pyke import knowledge_engine

engine = knowledge_engine.engine(__file__)

# Facts
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

# Rules
engine.add_rule('rules', 
    ('is_green', '?x', True),
    lambda fc, sc, ?x: [('visits', ?x, 'tiger', True)],
    ('foreach1', ['bear', 'cow', 'rabbit', 'tiger'])

engine.add_rule('rules',
    ('sees', '?x', 'bear', True),
    ('is_cold', '?x', True),
    lambda fc, sc, ?x: [('is_green', 'bear', True)],
    ('foreach2', ['bear', 'cow', 'rabbit', 'tiger'])

engine.add_rule('rules',
    ('needs', 'cow', 'rabbit', True),
    ('needs', 'rabbit', 'cow', True),
    lambda fc, sc: [('is_red', 'rabbit', True)],
    ('rule3', [])

engine.add_rule('rules',
    ('is_green', '?x', True),
    lambda fc, sc, ?x: [('needs', ?x, 'cow', True)],
    ('foreach4', ['bear', 'cow', 'rabbit', 'tiger'])

engine.add_rule('rules',
    ('visits', '?x', 'tiger', True),
    lambda fc, sc, ?x: [('is_red', 'tiger', True)],
    ('foreach5', ['bear', 'cow', 'rabbit', 'tiger'])

engine.add_rule('rules',
    ('needs', '?x', 'tiger', True),
    ('sees', 'tiger', 'cow', True),
    lambda fc, sc, ?x: [('needs', 'cow', 'bear', True)],
    ('foreach6', ['bear', 'cow', 'rabbit', 'tiger'])

engine.add_rule('rules',
    ('sees', '?x', 'bear', True),
    ('needs', '?x', 'bear', True),
    lambda fc, sc, ?x: [('sees', '?x', 'cow', True)],
    ('foreach7', ['bear', 'cow', 'rabbit', 'tiger'])

engine.add_rule('rules',
    ('visits', '?x', 'rabbit', True),
    lambda fc, sc, ?x: [('needs', 'rabbit', 'tiger', True)],
    ('foreach8', ['bear', 'cow', 'rabbit', 'tiger'])

engine.add_rule('rules',
    ('needs', '?x', 'bear', True),
    ('visits', 'bear', 'tiger', True),
    lambda fc, sc, ?x: [('sees', '?x', 'bear', True)],
    ('foreach9', ['bear', 'cow', 'rabbit', 'tiger'])

# Query
result = engine.prove_1('facts', ('visits', 'cow', 'rabbit', True), 1)
print(result is not None)