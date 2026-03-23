from pyke import knowledge_engine

# Create knowledge engine instance
engine = knowledge_engine.engine(__file__)

# Add facts
engine.add_casefact('facts', 'chases', ('bald_eagle', 'cat'))
engine.add_casefact('facts', 'is_young', ('bald_eagle',))
engine.add_casefact('facts', 'is_rough', ('cat',))
engine.add_casefact('facts', 'is_young', ('cat',))
engine.add_casefact('facts', 'sees', ('cat', 'bald_eagle'))
engine.add_casefact('facts', 'chases', ('lion', 'bald_eagle'))
engine.add_casefact('facts', 'chases', ('lion', 'cat'))
engine.add_casefact('facts', 'eats', ('lion', 'bald_eagle'))
engine.add_casefact('facts', 'eats', ('lion', 'cat'))
engine.add_casefact('facts', 'chases', ('mouse', 'bald_eagle'))
engine.add_casefact('facts', 'chases', ('mouse', 'lion'))
engine.add_casefact('facts', 'eats', ('mouse', 'bald_eagle'))
engine.add_casefact('facts', 'is_young', ('mouse',))

# Add rules
@engine.rule
def is_kind_implies_is_round():
    """
    If something is kind then it is round.
    """
    return (
        ('facts', 'is_kind', '?x'),
        (),
        [('facts', 'is_round', '?x')]
    )

@engine.rule
def chases_bald_eagle_implies_is_round():
    """
    If something chases the bald eagle then it is round.
    """
    return (
        ('facts', 'chases', '?x', 'bald_eagle'),
        (),
        [('facts', 'is_round', '?x')]
    )

@engine.rule
def is_round_implies_sees_bald_eagle():
    """
    If something is round then it sees the bald eagle.
    """
    return (
        ('facts', 'is_round', '?x'),
        (),
        [('facts', 'sees', '?x', 'bald_eagle')]
    )

@engine.rule
def chases_cat_and_cat_chases_bald_eagle_implies_eats_bald_eagle():
    """
    If something chases the cat and the cat chases the bald eagle then it eats the bald eagle.
    """
    return (
        ('facts', 'chases', '?x', 'cat'),
        ('facts', 'chases', 'cat', 'bald_eagle'),
        [('facts', 'eats', '?x', 'bald_eagle')]
    )

@engine.rule
def chases_cat_implies_cat_sees_lion():
    """
    If something chases the cat then the cat sees the lion.
    """
    return (
        ('facts', 'chases', '?x', 'cat'),
        (),
        [('facts', 'sees', 'cat', 'lion')]
    )

@engine.rule
def sees_cat_implies_chases_bald_eagle():
    """
    If something sees the cat then it chases the bald eagle.
    """
    return (
        ('facts', 'sees', '?x', 'cat'),
        (),
        [('facts', 'chases', '?x', 'bald_eagle')]
    )

@engine.rule
def young_bald_eagle_chases_lion_implies_sees_lion():
    """
    If the bald eagle is young and the bald eagle chases the lion then the bald eagle sees the lion.
    """
    return (
        ('facts', 'is_young', 'bald_eagle'),
        ('facts', 'chases', 'bald_eagle', 'lion'),
        [('facts', 'sees', 'bald_eagle', 'lion')]
    )

@engine.rule
def mouse_eats_cat_and_bald_eagle_implies_bald_eagle_eats_cat():
    """
    If the mouse eats the cat and the mouse eats the bald eagle then the bald eagle eats the cat.
    """
    return (
        ('facts', 'eats', 'mouse', 'cat'),
        ('facts', 'eats', 'mouse', 'bald_eagle'),
        [('facts', 'eats', 'bald_eagle', 'cat')]
    )

@engine.rule
def sees_bald_eagle_and_chases_cat_implies_bald_eagle_sees_cat():
    """
    If something sees the bald eagle and it chases the cat then the bald eagle sees the cat.
    """
    return (
        ('facts', 'sees', '?x', 'bald_eagle'),
        ('facts', 'chases', '?x', 'cat'),
        [('facts', 'sees', 'bald_eagle', 'cat')]
    )

# Activate the knowledge base
engine.activate('kb')

# Query: does the cat see the lion?
result = engine.query('facts', 'sees', ('cat', 'lion'))
print(result)