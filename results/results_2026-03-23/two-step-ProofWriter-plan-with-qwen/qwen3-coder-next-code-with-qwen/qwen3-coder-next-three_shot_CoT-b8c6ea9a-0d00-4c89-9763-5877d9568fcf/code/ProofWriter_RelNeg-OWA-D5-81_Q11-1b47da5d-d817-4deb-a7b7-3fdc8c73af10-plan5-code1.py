from pyke import knowledge_engine

engine = knowledge_engine.engine(__file__)

# Facts
engine.add_case_fact('kb', 'eats', ('cat', 'squirrel', True))
engine.add_case_fact('kb', 'sees', ('cat', 'squirrel', True))
engine.add_case_fact('kb', 'eats', ('cow', 'squirrel', True))
engine.add_case_fact('kb', 'sees', ('cow', 'cat', True))
engine.add_case_fact('kb', 'is_round', ('rabbit', True))
engine.add_case_fact('kb', 'sees', ('rabbit', 'cat', True))
engine.add_case_fact('kb', 'eats', ('squirrel', 'rabbit', True))
engine.add_case_fact('kb', 'is_cold', ('squirrel', True))
engine.add_case_fact('kb', 'needs', ('squirrel', 'rabbit', True))
engine.add_case_fact('kb', 'sees', ('squirrel', 'cat', True))

# Rules
engine.add_rule('kb',
    ('sees', '?x', 'cat', True),
    ('not', ('is_green', '?x', True)),
    ('sees', '?x', 'cow', True))

engine.add_rule('kb',
    ('is_rough', '?x', True),
    ('is_cold', '?x', True))

engine.add_rule('kb',
    ('sees', '?x', 'rabbit', True),
    ('not', ('is_round', '?x', True)))

engine.add_rule('kb',
    ('sees', '?x', 'squirrel', True),
    ('not', ('is_green', '?x', True)),
    ('needs', '?x', 'squirrel', True))

engine.add_rule('kb',
    ('eats', '?x', 'cow', True),
    ('sees', '?x', 'rabbit', True))

engine.add_rule('kb',
    ('eats', '?x', 'squirrel', True),
    ('is_rough', '?x', True))

engine.add_rule('kb',
    ('is_cold', '?x', True),
    ('eats', '?x', 'cow', True))

# Query: Is the cat not round?
result = engine.prove_1('kb', 'is_round', ('cat', True), 0)
if result is None:
    # If we cannot prove cat is round, then cat is not round
    print("True")
else:
    # If we can prove cat is round, then the statement "cat is not round" is false
    print("False")