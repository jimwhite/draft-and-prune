from pyke import knowledge_engine

engine = knowledge_engine.engine(__file__)

# --- Facts ---
engine.add_case_fact('kb', ('needs', 'cat', 'dog'))
engine.add_case_fact('kb', ('is_kind', 'dog'))
engine.add_case_fact('kb', ('needs', 'dog', 'rabbit'))
engine.add_case_fact('kb', ('eats', 'rabbit', 'dog'))
engine.add_case_fact('kb', ('is_green', 'rabbit'))
engine.add_case_fact('kb', ('chases', 'tiger', 'rabbit'))
engine.add_case_fact('kb', ('is_big', 'tiger'))

# --- Rules ---
engine.add_rule('kb',
    ('is_nice', '?x'),
    ('eats', '?x', 'tiger'),
    ('needs', '?x', 'dog')
)

engine.add_rule('kb',
    ('chases', '?x', 'cat'),
    ('eats', '?x', 'cat')
)

engine.add_rule('kb',
    ('chases', 'dog', 'tiger'),
    ('needs', 'tiger', 'rabbit')
)

engine.add_rule('kb',
    ('chases', 'rabbit', 'tiger'),
    ('chases', 'rabbit', 'cat')
)

engine.add_rule('kb',
    ('chases', '?x', 'cat'),
    ('is_kind', 'cat')
)

engine.add_rule('kb',
    ('eats', '?x', 'dog'),
    ('chases', '?x', 'cat')
)

engine.add_rule('kb',
    ('is_rough', '?x'),
    ('eats', '?x', 'dog')
)

engine.add_rule('kb',
    ('is_kind', '?x'),
    ('is_rough', '?x')
)

engine.add_rule('kb',
    ('eats', '?x', 'rabbit'),
    ('is_big', 'rabbit'),
    ('is_kind', '?x')
)

# --- Query ---
engine.activate('kb')
result = engine.prove_1_goal('kb', ('is_rough', 'cat'))
# Since we want to check if cat is NOT rough, we need to see if is_rough('cat') fails
# If prove_1_goal returns None (fails), then cat is not rough → True
# If it succeeds, then cat is rough → False

print("cat is rough:", result is not None)
# The statement "The cat is not rough" is True if prove_1_goal fails