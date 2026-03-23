from pyke import knowledge_engine

engine = knowledge_engine.engine(__file__)

# Facts section
engine.add_case_fact('facts', ('is_smart', 'Anne', True))
engine.add_case_fact('facts', ('is_nice', 'Charlie', True))
engine.add_case_fact('facts', ('is_furry', 'Erin', True))
engine.add_case_fact('facts', ('is_white', 'Erin', True))
engine.add_case_fact('facts', ('is_smart', 'Fiona', True))
engine.add_case_fact('facts', ('is_white', 'Fiona', True))
engine.add_case_fact('facts', ('is_young', 'Fiona', True))

# Rules section
engine.add_rule('nice_and_smart_are_young',
    ('is_nice', '$x', True),
    ('is_smart', '$x', True),
    ('is_young', '$x', True))

engine.add_rule('young_and_white_are_cold',
    ('is_young', '$x', True),
    ('is_white', '$x', True),
    ('is_cold', '$x', True))

engine.add_rule('white_are_red',
    ('is_white', '$x', True),
    ('is_red', '$x', True))

engine.add_rule('furry_and_red_are_nice',
    ('is_furry', '$x', True),
    ('is_red', '$x', True),
    ('is_nice', '$x', True))

engine.add_rule('young_are_white',
    ('is_young', '$x', True),
    ('is_white', '$x', True))

engine.add_rule('smart_and_cold_are_furry',
    ('is_smart', '$x', True),
    ('is_cold', '$x', True),
    ('is_furry', '$x', True))

engine.add_rule('nice_and_white_are_smart',
    ('is_nice', '$x', True),
    ('is_white', '$x', True),
    ('is_smart', '$x', True))

engine.add_rule('anne_furry_and_white_is_red',
    ('is_furry', 'Anne', True),
    ('is_white', 'Anne', True),
    ('is_red', 'Anne', True))

# Query section
engine.activate('facts')

# Check if Erin is cold
result = engine.query(('is_cold', 'Erin', True))
print(result)