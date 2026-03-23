from pyke import knowledge_engine

engine = knowledge_engine.engine(__file__)

# Facts
engine.add_case_fact('facts', ('chases', 'bald_eagle', 'cat', True))
engine.add_case_fact('facts', ('not_chases', 'bald_eagle', 'mouse', True))
engine.add_case_fact('facts', ('is_young', 'bald_eagle', True))
engine.add_case_fact('facts', ('not_chases', 'cat', 'bald_eagle', True))
engine.add_case_fact('facts', ('not_eats', 'cat', 'bald_eagle', True))
engine.add_case_fact('facts', ('is_rough', 'cat', True))
engine.add_case_fact('facts', ('is_young', 'cat', True))
engine.add_case_fact('facts', ('sees', 'cat', 'bald_eagle', True))
engine.add_case_fact('facts', ('chases', 'lion', 'bald_eagle', True))
engine.add_case_fact('facts', ('chases', 'lion', 'cat', True))
engine.add_case_fact('facts', ('eats', 'lion', 'bald_eagle', True))
engine.add_case_fact('facts', ('eats', 'lion', 'cat', True))
engine.add_case_fact('facts', ('chases', 'mouse', 'bald_eagle', True))
engine.add_case_fact('facts', ('chases', 'mouse', 'lion', True))
engine.add_case_fact('facts', ('eats', 'mouse', 'bald_eagle', True))
engine.add_case_fact('facts', ('is_young', 'mouse', True))

# Rules
@engine.rule
def kind_to_round():
    return (
        ('facts', 'is_kind', '?x', True),
        (),
        [('facts', 'is_round', '?x', True)]
    )

@engine.rule
def chases_bald_eagle_to_round():
    return (
        ('facts', 'chases', '?x', 'bald_eagle', True),
        (),
        [('facts', 'is_round', '?x', True)]
    )

@engine.rule
def round_to_sees_bald_eagle():
    return (
        ('facts', 'is_round', '?x', True),
        (),
        [('facts', 'sees', '?x', 'bald_eagle', True)]
    )

@engine.rule
def chases_cat_and_cat_chases_bald_eagle_to_eats_bald_eagle():
    return (
        ('facts', 'chases', '?x', 'cat', True),
        ('facts', 'chases', 'cat', 'bald_eagle', True),
        [('facts', 'eats', '?x', 'bald_eagle', True)]
    )

@engine.rule
def chases_cat_to_cat_sees_lion():
    return (
        ('facts', 'chases', '?x', 'cat', True),
        (),
        [('facts', 'sees', 'cat', 'lion', True)]
    )

@engine.rule
def sees_cat_to_chases_bald_eagle():
    return (
        ('facts', 'sees', '?x', 'cat', True),
        (),
        [('facts', 'chases', '?x', 'bald_eagle', True)]
    )

@engine.rule
def young_bald_eagle_chases_lion_to_sees_lion():
    return (
        ('facts', 'is_young', 'bald_eagle', True),
        ('facts', 'chases', 'bald_eagle', 'lion', True),
        [('facts', 'sees', 'bald_eagle', 'lion', True)]
    )

@engine.rule
def mouse_eats_cat_and_bald_eagle_to_bald_eagle_eats_cat():
    return (
        ('facts', 'eats', 'mouse', 'cat', True),
        ('facts', 'eats', 'mouse', 'bald_eagle', True),
        [('facts', 'eats', 'bald_eagle', 'cat', True)]
    )

@engine.rule
def sees_bald_eagle_and_chases_cat_to_bald_eagle_sees():
    return (
        ('facts', 'sees', '?x', 'bald_eagle', True),
        ('facts', 'chases', '?x', 'cat', True),
        [('facts', 'sees', 'bald_eagle', '?x', True)]
    )

# Query
engine.activate('facts')
result = engine.prove_1('facts', 'sees', ('cat', 'lion', True), None)
print(result is not None)