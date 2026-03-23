from pyke import knowledge_engine

engine = knowledge_engine.engine(__file__)

# Facts
engine.add_case_fact('kb', ('is_smart', 'Anne', True))
engine.add_case_fact('kb', ('is_nice', 'Charlie', True))
engine.add_case_fact('kb', ('is_furry', 'Erin', True))
engine.add_case_fact('kb', ('is_white', 'Erin', True))
engine.add_case_fact('kb', ('is_smart', 'Fiona', True))
engine.add_case_fact('kb', ('is_white', 'Fiona', True))
engine.add_case_fact('kb', ('is_young', 'Fiona', True))

# Rules
engine.add_rule('kb', 
    ('is_nice', '$x', True),
    ('is_smart', '$x', True),
    ('is_young', '$x', True))

engine.add_rule('kb',
    ('is_young', '$x', True),
    ('is_white', '$x', True),
    ('is_cold', '$x', True))

engine.add_rule('kb',
    ('is_white', '$x', True),
    ('is_red', '$x', True))

engine.add_rule('kb',
    ('is_furry', '$x', True),
    ('is_red', '$x', True),
    ('is_nice', '$x', True))

engine.add_rule('kb',
    ('is_young', '$x', True),
    ('is_white', '$x', True))

engine.add_rule('kb',
    ('is_smart', '$x', True),
    ('is_cold', '$x', True),
    ('is_furry', '$x', True))

engine.add_rule('kb',
    ('is_nice', '$x', True),
    ('is_white', '$x', True),
    ('is_smart', '$x', True))

engine.add_rule('kb',
    ('eq', '$x', 'Anne'),
    ('is_furry', '$x', True),
    ('is_white', '$x', True),
    ('is_red', '$x', True))

# Query
result = engine.prove_1('kb', ('is_cold', 'Erin', True), None)
print(result is not None)