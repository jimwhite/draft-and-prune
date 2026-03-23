from pyke import knowledge_engine

engine = knowledge_engine.engine(__file__)

# Facts
engine.add_case_fact('kb', ('is_blue', 'Anne', True))
engine.add_case_fact('kb', ('is_cold', 'Anne', True))
engine.add_case_fact('kb', ('is_kind', 'Anne', True))
engine.add_case_fact('kb', ('is_quiet', 'Anne', True))

engine.add_case_fact('kb', ('is_blue', 'Bob', True))
engine.add_case_fact('kb', ('is_kind', 'Bob', True))
engine.add_case_fact('kb', ('is_nice', 'Bob', True))
engine.add_case_fact('kb', ('is_quiet', 'Bob', False))

engine.add_case_fact('kb', ('is_furry', 'Dave', False))
engine.add_case_fact('kb', ('is_green', 'Dave', True))
engine.add_case_fact('kb', ('is_quiet', 'Dave', True))

engine.add_case_fact('kb', ('is_cold', 'Fiona', True))

# Rules
engine.add_rule('kb',
    ('is_cold', '?x', True),
    (),
    ('is_blue', '?x', True)
)

engine.add_rule('kb',
    ('is_green', '?x', True),
    ('is_nice', '?x', True),
    ('is_kind', '?x', True)
)

engine.add_rule('kb',
    ('is_blue', '?x', True),
    (),
    ('is_kind', '?x', True)
)

engine.add_rule('kb',
    ('is_kind', '?x', True),
    ('is_cold', '?x', True),
    ('is_nice', '?x', True)
)

engine.add_rule('kb',
    ('is_nice', '?x', True),
    (),
    ('is_green', '?x', True)
)

engine.add_rule('kb',
    ('is_cold', '?x', True),
    ('is_green', '?x', True),
    ('is_quiet', '?x', True)
)

# Query
result = engine.query('kb').goal(('is_kind', 'Fiona', False))
print("Fiona is not kind:", result)