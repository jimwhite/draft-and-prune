from pyke import knowledge_engine

engine = knowledge_engine.engine(__file__)

# Facts
engine.add_case_fact('facts', ('is_kind', 'Bob', True))
engine.add_case_fact('facts', ('is_quiet', 'Charlie', True))
engine.add_case_fact('facts', ('is_rough', 'Charlie', True))
engine.add_case_fact('facts', ('is_kind', 'Fiona', True))
engine.add_case_fact('facts', ('is_rough', 'Fiona', True))
engine.add_case_fact('facts', ('is_white', 'Fiona', True))
engine.add_case_fact('facts', ('is_nice', 'Gary', True))

# Rules
@engine.rule('rules')
def nice_to_white():
    return (
        ('facts', 'is_nice', '?x', True),
        lambda: engine.add_case_fact('facts', ('is_white', '?x', True))
    )

@engine.rule('rules')
def white_to_rough():
    return (
        ('facts', 'is_white', '?x', True),
        lambda: engine.add_case_fact('facts', ('is_rough', '?x', True))
    )

@engine.rule('rules')
def rough_to_red():
    return (
        ('facts', 'is_rough', '?x', True),
        lambda: engine.add_case_fact('facts', ('is_red', '?x', True))
    )

@engine.rule('rules')
def red_white_to_quiet():
    return (
        ('facts', 'is_red', '?x', True),
        ('facts', 'is_white', '?x', True),
        lambda: engine.add_case_fact('facts', ('is_quiet', '?x', True))
    )

@engine.rule('rules')
def smart_to_white():
    return (
        ('facts', 'is_smart', '?x', True),
        lambda: engine.add_case_fact('facts', ('is_white', '?x', True))
    )

@engine.rule('rules')
def rough_quiet_not_kind():
    return (
        ('facts', 'is_rough', '?x', True),
        ('facts', 'is_quiet', '?x', True),
        lambda: engine.add_case_fact('facts', ('is_kind', '?x', False))
    )

@engine.rule('rules')
def quiet_not_smart_to_kind():
    return (
        ('facts', 'is_quiet', '?x', True),
        ('facts', 'is_smart', '?x', False),
        lambda: engine.add_case_fact('facts', ('is_kind', '?x', True))
    )

@engine.rule('rules')
def smart_to_quiet():
    return (
        ('facts', 'is_smart', '?x', True),
        lambda: engine.add_case_fact('facts', ('is_quiet', '?x', True))
    )

@engine.rule('rules')
def smart_not_rough_to_quiet():
    return (
        ('facts', 'is_smart', '?x', True),
        ('facts', 'is_rough', '?x', False),
        lambda: engine.add_case_fact('facts', ('is_quiet', '?x', True))
    )

# Run the engine to apply all rules
engine.activate('rules')

# Query: is Gary not quiet?
result = engine.query(('facts', 'is_quiet', 'Gary', False))
print("True" if result else "False")