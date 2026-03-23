from pyke import knowledge_engine

engine = knowledge_engine.engine(__file__)

# Facts:
engine.add_case_fact('kb', ('is_young', 'Charlie', True))
engine.add_case_fact('kb', ('is_blue', 'Erin', True))
engine.add_case_fact('kb', ('is_kind', 'Erin', False))
engine.add_case_fact('kb', ('is_blue', 'Fiona', True))
engine.add_case_fact('kb', ('is_white', 'Fiona', True))
engine.add_case_fact('kb', ('is_blue', 'Gary', True))
engine.add_case_fact('kb', ('is_kind', 'Gary', True))

# Rules:
# Furry, nice things are white.
engine.add_rule('kb', 
    ('is_furry', '?x', True),
    ('is_nice', '?x', True),
    ('is_white', '?x', True))

# If something is young and blue then it is smart.
engine.add_rule('kb',
    ('is_young', '?x', True),
    ('is_blue', '?x', True),
    ('is_smart', '?x', True))

# All blue, smart things are furry.
engine.add_rule('kb',
    ('is_blue', '?x', True),
    ('is_smart', '?x', True),
    ('is_furry', '?x', True))

# All smart, white things are furry.
engine.add_rule('kb',
    ('is_smart', '?x', True),
    ('is_white', '?x', True),
    ('is_furry', '?x', True))

# Young things are nice.
engine.add_rule('kb',
    ('is_young', '?x', True),
    ('is_nice', '?x', True))

# If Fiona is smart and Fiona is young then Fiona is not furry.
engine.add_rule('kb',
    ('is_smart', 'Fiona', True),
    ('is_young', 'Fiona', True),
    ('is_furry', 'Fiona', False))

# If Erin is kind then Erin is furry.
engine.add_rule('kb',
    ('is_kind', 'Erin', True),
    ('is_furry', 'Erin', True))

# If Gary is smart and Gary is white then Gary is not kind.
engine.add_rule('kb',
    ('is_smart', 'Gary', True),
    ('is_white', 'Gary', True),
    ('is_kind', 'Gary', False))

# If something is nice then it is blue.
engine.add_rule('kb',
    ('is_nice', '?x', True),
    ('is_blue', '?x', True))

# Query:
result = engine.prove_1('kb', ('is_white', 'Fiona', False), 1)
print("Query: Fiona is not white")
if result:
    print("False - Fiona IS white (so 'Fiona is not white' is false)")
else:
    print("Unknown or False - Fiona is not white cannot be proven")