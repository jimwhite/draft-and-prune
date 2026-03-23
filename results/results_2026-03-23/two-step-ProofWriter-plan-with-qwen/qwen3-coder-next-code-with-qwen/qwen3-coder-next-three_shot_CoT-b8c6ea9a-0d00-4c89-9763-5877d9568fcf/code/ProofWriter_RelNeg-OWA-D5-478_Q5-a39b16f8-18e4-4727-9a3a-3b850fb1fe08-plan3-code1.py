from pyke import knowledge_engine

engine = knowledge_engine.engine(__file__)

# Facts
engine.add_case_fact('facts', ('is_kind', 'cow', True))
engine.add_case_fact('facts', ('sees', 'cow', 'mouse', True))
engine.add_case_fact('facts', ('eats', 'mouse', 'cow', True))
engine.add_case_fact('facts', ('is_kind', 'mouse', True))
engine.add_case_fact('facts', ('needs', 'mouse', 'squirrel', True))
engine.add_case_fact('facts', ('eats', 'rabbit', 'mouse', True))
engine.add_case_fact('facts', ('is_blue', 'rabbit', False))
engine.add_case_fact('facts', ('is_blue', 'squirrel', False))
engine.add_case_fact('facts', ('is_green', 'squirrel', True))
engine.add_case_fact('facts', ('is_rough', 'squirrel', True))
engine.add_case_fact('facts', ('needs', 'squirrel', 'mouse', True))
engine.add_case_fact('facts', ('sees', 'squirrel', 'rabbit', True))

# Rules
@engine.rule('rules')
def sees_cow_implies_sees_squirrel():
    return (
        ('sees', '?x', 'cow', True),
        [('sees', '?x', 'squirrel', True)]
    )

@engine.rule('rules')
def sees_rabbit_implies_eats_cow():
    return (
        ('sees', '?x', 'rabbit', True),
        [('eats', '?x', 'cow', True)]
    )

@engine.rule('rules')
def needs_cow_implies_cow_eats_mouse():
    return (
        ('needs', '?x', 'cow', True),
        [('eats', 'cow', 'mouse', True)]
    )

@engine.rule('rules')
def needs_squirrel_and_squirrel_needs_cow_implies_cow_not_needs_rabbit():
    return (
        ('needs', '?x', 'squirrel', True),
        ('needs', 'squirrel', 'cow', True),
        [('not', ('needs', 'cow', 'rabbit', True))]
    )

@engine.rule('rules')
def mouse_eats_rabbit_and_rabbit_not_see_mouse_implies_rabbit_green():
    return (
        ('eats', 'mouse', 'rabbit', True),
        ('not', ('sees', 'rabbit', 'mouse', True)),
        [('is_green', 'rabbit', True)]
    )

@engine.rule('rules')
def cow_needs_rabbit_implies_rabbit_not_eats_mouse():
    return (
        ('needs', 'cow', 'rabbit', True),
        [('not', ('eats', 'rabbit', 'mouse', True))]
    )

@engine.rule('rules')
def eats_squirrel_and_squirrel_eats_cow_implies_needs_cow():
    return (
        ('eats', '?x', 'squirrel', True),
        ('eats', 'squirrel', 'cow', True),
        [('needs', '?x', 'cow', True)]
    )

@engine.rule('rules')
def eats_mouse_implies_eats_squirrel():
    return (
        ('eats', '?x', 'mouse', True),
        [('eats', '?x', 'squirrel', True)]
    )

# Query
engine.activate('rules')
result = engine.prove_1('facts', ('needs', 'rabbit', 'cow', True), None)
print("True" if result else "False")