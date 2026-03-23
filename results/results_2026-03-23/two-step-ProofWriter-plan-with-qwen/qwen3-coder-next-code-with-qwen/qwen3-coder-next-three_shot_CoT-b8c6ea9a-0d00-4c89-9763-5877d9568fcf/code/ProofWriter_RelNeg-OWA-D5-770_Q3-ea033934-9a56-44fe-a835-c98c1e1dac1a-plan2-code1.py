from pyke import knowledge_engine

engine = knowledge_engine.engine(__file__)

# Facts
engine.add_predicate('chases', 2)
engine.add_predicate('eats', 2)
engine.add_predicate('is_rough', 1)
engine.add_predicate('is_young', 1)
engine.add_predicate('sees', 2)

# Explicitly stated facts
engine.assert_('chases', 'bald_eagle', 'cat')
engine.assert_('chases', 'lion', 'bald_eagle')
engine.assert_('chases', 'lion', 'cat')
engine.assert_('chases', 'mouse', 'bald_eagle')
engine.assert_('chases', 'mouse', 'lion')
engine.assert_('eats', 'lion', 'bald_eagle')
engine.assert_('eats', 'lion', 'cat')
engine.assert_('eats', 'mouse', 'bald_eagle')
engine.assert_('is_rough', 'cat')
engine.assert_('is_young', 'bald_eagle')
engine.assert_('is_young', 'cat')
engine.assert_('is_young', 'mouse')
engine.assert_('sees', 'cat', 'bald_eagle')

# Rules
@engine.rule('rule1')
def kind_to_round():
    return (
        ('is_kind', '?x'),
        '=>',
        ('is_round', '?x')
    )

@engine.rule('rule2')
def chases_bald_eagle_to_round():
    return (
        ('chases', '?x', 'bald_eagle'),
        '=>',
        ('is_round', '?x')
    )

@engine.rule('rule3')
def round_to_sees_bald_eagle():
    return (
        ('is_round', '?x'),
        '=>',
        ('sees', '?x', 'bald_eagle')
    )

@engine.rule('rule4')
def chase_cat_and_cat_chases_bald_eagle_to_eats_bald_eagle():
    return (
        ('chases', '?x', 'cat'),
        ('chases', 'cat', 'bald_eagle'),
        '=>',
        ('eats', '?x', 'bald_eagle')
    )

@engine.rule('rule5')
def chase_cat_then_cat_sees_lion():
    return (
        ('chases', '?x', 'cat'),
        '=>',
        ('sees', 'cat', 'lion')
    )

@engine.rule('rule6')
def sees_cat_then_chases_bald_eagle():
    return (
        ('sees', '?x', 'cat'),
        '=>',
        ('chases', '?x', 'bald_eagle')
    )

@engine.rule('rule7')
def young_bald_eagle_chases_lion_then_sees_lion():
    return (
        ('is_young', 'bald_eagle'),
        ('chases', 'bald_eagle', 'lion'),
        '=>',
        ('sees', 'bald_eagle', 'lion')
    )

@engine.rule('rule8')
def mouse_eats_cat_and_bald_eagle_then_bald_eagle_eats_cat():
    return (
        ('eats', 'mouse', 'cat'),
        ('eats', 'mouse', 'bald_eagle'),
        '=>',
        ('eats', 'bald_eagle', 'cat')
    )

@engine.rule('rule9')
def sees_bald_eagle_and_chases_cat_then_bald_eagle_sees_it():
    return (
        ('sees', '?x', 'bald_eagle'),
        ('chases', '?x', 'cat'),
        '=>',
        ('sees', 'bald_eagle', '?x')
    )

# Query
engine.query(('sees', 'cat', 'lion'))