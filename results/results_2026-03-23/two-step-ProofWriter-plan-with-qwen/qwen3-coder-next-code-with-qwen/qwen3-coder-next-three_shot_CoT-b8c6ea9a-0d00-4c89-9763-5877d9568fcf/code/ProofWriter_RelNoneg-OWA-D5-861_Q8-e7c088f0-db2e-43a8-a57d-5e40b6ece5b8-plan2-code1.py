from pyke import knowledge_engine

engine = knowledge_engine.engine(__file__)

# --- Facts ---
engine.add_case_fact('facts', ('needs', 'cat', 'dog'))
engine.add_case_fact('facts', ('is_kind', 'dog'))
engine.add_case_fact('facts', ('needs', 'dog', 'rabbit'))
engine.add_case_fact('facts', ('eats', 'rabbit', 'dog'))
engine.add_case_fact('facts', ('is_green', 'rabbit'))
engine.add_case_fact('facts', ('chases', 'tiger', 'rabbit'))
engine.add_case_fact('facts', ('is_big', 'tiger'))

# --- Rules ---
engine.add_rule('rules', 
    ('nice', '?x'),
    ('eats', '?x', 'tiger'),
    ('needs', '?x', 'dog'))

engine.add_rule('rules',
    ('chases', '?x', 'cat'),
    ('eats', '?x', 'cat'))

engine.add_rule('rules',
    ('chases', 'dog', 'tiger'),
    ('needs', 'tiger', 'rabbit'))

engine.add_rule('rules',
    ('chases', 'rabbit', 'tiger'),
    ('chases', 'rabbit', 'cat'))

engine.add_rule('rules',
    ('chases', '?x', 'cat'),
    ('is_kind', 'cat'))

engine.add_rule('rules',
    ('eats', '?x', 'dog'),
    ('chases', '?x', 'cat'))

engine.add_rule('rules',
    ('is_rough', '?x'),
    ('eats', '?x', 'dog'))

engine.add_rule('rules',
    ('is_kind', '?x'),
    ('is_rough', '?x'))

engine.add_rule('rules',
    ('eats', '?x', 'rabbit'),
    ('is_big', 'rabbit'),
    ('is_kind', '?x'))

# --- Query ---
try:
    result = engine.prove_1('facts', 'is_rough', ('cat',), 1)
    # If we can prove is_rough("cat") is true, then "the cat is not rough" is false
    # If we can't prove it and have no evidence to the contrary, it's unknown
    if result:
        print("false")
    else:
        # Check if we can prove it's false (not rough)
        try:
            result_false = engine.prove_1('facts', 'is_rough', ('cat',), 1, 
                                        goal_stmt=('not', ('is_rough', 'cat')))
            print("true")
        except:
            print("unknown")
except Exception as e:
    # If there's an error in proving, it's likely unknown
    print("unknown")