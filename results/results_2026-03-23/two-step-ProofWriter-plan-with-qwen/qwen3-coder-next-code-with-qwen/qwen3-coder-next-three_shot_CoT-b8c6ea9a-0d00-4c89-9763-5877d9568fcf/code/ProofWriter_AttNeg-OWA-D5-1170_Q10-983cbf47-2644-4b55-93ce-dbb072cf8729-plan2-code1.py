from pyke import knowledge_engine, facts, rules

engine = knowledge_engine.engine(__file__)

# Facts
engine.add_case_fact('kb', ('is_kind', 'Bob', True))
engine.add_case_fact('kb', ('is_quiet', 'Charlie', True))
engine.add_case_fact('kb', ('is_rough', 'Charlie', True))
engine.add_case_fact('kb', ('is_kind', 'Fiona', True))
engine.add_case_fact('kb', ('is_rough', 'Fiona', True))
engine.add_case_fact('kb', ('is_white', 'Fiona', True))
engine.add_case_fact('kb', ('is_nice', 'Gary', True))

# Rules
@rules.rule(
    'kb',
    ('is_red', 'Gary', True),
    ('is_white', 'Gary', True)
)
def gary_red_white_to_quiet(kb):
    kb.assert_fact('kb', ('is_quiet', 'Gary', True))

@rules.rule(
    'kb',
    ('is_white', '$x', True)
)
def white_to_rough(kb, x):
    kb.assert_fact('kb', ('is_rough', x, True))

@rules.rule(
    'kb',
    ('is_rough', '$x', True)
)
def rough_to_red(kb, x):
    kb.assert_fact('kb', ('is_red', x, True))

@rules.rule(
    'kb',
    ('is_nice', '$x', True)
)
def nice_to_white(kb, x):
    kb.assert_fact('kb', ('is_white', x, True))

@rules.rule(
    'kb',
    ('is_smart', '$x', True)
)
def smart_to_white(kb, x):
    kb.assert_fact('kb', ('is_white', x, True))

@rules.rule(
    'kb',
    ('is_rough', '$x', True),
    ('is_quiet', '$x', True)
)
def rough_quiet_not_kind(kb, x):
    kb.assert_fact('kb', ('is_kind', x, False))

@rules.rule(
    'kb',
    ('is_quiet', '$x', True),
    ('is_smart', '$x', False)
)
def quiet_not_smart_to_kind(kb, x):
    kb.assert_fact('kb', ('is_kind', x, True))

@rules.rule(
    'kb',
    ('is_smart', '$x', True)
)
def smart_to_quiet(kb, x):
    kb.assert_fact('kb', ('is_quiet', x, True))

@rules.rule(
    'kb',
    ('is_smart', '$x', True),
    ('is_rough', '$x', False)
)
def smart_not_rough_to_quiet(kb, x):
    kb.assert_fact('kb', ('is_quiet', x, True))

# Query
engine.activate('kb')
result = engine.query('kb', ('is_quiet', 'Gary', False))
print("Result:", result)