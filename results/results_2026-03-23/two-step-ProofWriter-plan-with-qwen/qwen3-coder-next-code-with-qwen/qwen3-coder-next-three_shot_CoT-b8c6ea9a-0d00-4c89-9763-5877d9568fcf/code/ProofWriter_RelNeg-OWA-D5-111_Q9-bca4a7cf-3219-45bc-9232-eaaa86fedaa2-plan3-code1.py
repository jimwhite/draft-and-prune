from pyke import knowledge_engine

# Initialize the knowledge engine
engine = knowledge_engine.engine(__file__)

# Facts: Only positive facts are asserted; negative statements are handled via rules
engine.add_universal_fact('domain', 'chases', ('bald_eagle', 'mouse'))
engine.add_universal_fact('domain', 'chases', ('bald_eagle', 'squirrel'))
engine.add_universal_fact('domain', 'is_cold', ('bald_eagle',))

engine.add_universal_fact('domain', 'chases', ('lion', 'bald_eagle'))
engine.add_universal_fact('domain', 'chases', ('lion', 'squirrel'))
engine.add_universal_fact('domain', 'is_blue', ('lion',))
engine.add_universal_fact('domain', 'needs', ('lion', 'squirrel'))
engine.add_universal_fact('domain', 'visits', ('lion', 'squirrel'))

# Mouse does not visit bald eagle or squirrel - handled via rules
# Squirrel does not visit lion - handled via rules

engine.add_universal_fact('domain', 'is_cold', ('squirrel',))
engine.add_universal_fact('domain', 'is_red', ('squirrel',))

# Rules
@engine.rule
def mouse_green_if_visited():
    """
    If something visits the mouse then the mouse is green.
    """
    return (
        ('domain', 'visits', '?x', 'mouse'),
        (),
        [('domain', 'is_green', 'mouse')]
    )

@engine.rule
def mouse_needs_lion_if_not_chasing():
    """
    If the mouse does not chase the lion then the mouse needs the lion.
    """
    return (
        # Check that mouse does not chase lion (i.e., no fact of mouse chasing lion)
        (),
        [('domain', 'chases', 'mouse', 'lion')],
        [('domain', 'needs', 'mouse', 'lion')]
    )

@engine.rule
def lion_green_if_visits_squirrel_and_squirrel_not_chasing_lion():
    """
    If something visits the squirrel and the squirrel does not chase the lion then the lion is green.
    """
    return (
        ('domain', 'visits', '?x', 'squirrel'),
        [('domain', 'chases', 'squirrel', 'lion')],
        [('domain', 'is_green', 'lion')]
    )

@engine.rule
def young_visits_bald_eagle():
    """
    If something is young then it visits the bald eagle.
    """
    return (
        ('domain', 'is_young', '?x'),
        (),
        [('domain', 'visits', '?x', 'bald_eagle')]
    )

@engine.rule
def visits_bald_eagle_then_visits_squirrel():
    """
    If something visits the bald eagle then the bald eagle visits the squirrel.
    """
    return (
        ('domain', 'visits', '?x', 'bald_eagle'),
        (),
        [('domain', 'visits', 'bald_eagle', 'squirrel')]
    )

@engine.rule
def visits_squirrel_and_red_then_young():
    """
    If something visits the squirrel and the squirrel is red then it is young.
    """
    return (
        ('domain', 'visits', '?x', 'squirrel'),
        [('domain', 'is_red', 'squirrel')],
        [('domain', 'is_young', '?x')]
    )

@engine.rule
def needs_squirrel_and_not_cold_then_squirrel_chases_bald_eagle():
    """
    If something needs the squirrel and it is not cold then the squirrel chases the bald eagle.
    """
    return (
        ('domain', 'needs', '?x', 'squirrel'),
        [('domain', 'is_cold', '?x')],
        [('domain', 'chases', 'squirrel', 'bald_eagle')]
    )

# Query
engine.add_universal_fact('domain', 'is_young', 'bald_eagle')