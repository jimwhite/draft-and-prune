from pyke import knowledge_engine, facts, rules

# Initialize knowledge engine
engine = knowledge_engine.engine(__file__)

# --- Facts ---
engine.add_case_fact('facts', ('is_cold', 'lion'))
engine.add_case_fact('facts', ('needs', 'squirrel', 'mouse'))
engine.add_case_fact('facts', ('needs', 'squirrel', 'rabbit'))
engine.add_case_fact('facts', ('is_kind', 'squirrel'))
engine.add_case_fact('facts', ('visits', 'lion', 'squirrel'))
engine.add_case_fact('facts', ('is_cold', 'mouse'))
engine.add_case_fact('facts', ('is_cold', 'rabbit'))
engine.add_case_fact('facts', ('is_rough', 'rabbit'))
engine.add_case_fact('facts', ('sees', 'squirrel', 'lion'))
# Note: The original says "The squirrel does not see the lion" and "does not see the rabbit"
# So we need to explicitly state these as false, but PyKe uses closed world assumption
# For negation, we'll use the facts that squirrel does NOT see lion/rabbit

# Since PyKe doesn't automatically assume false for unasserted facts,
# we need to handle negation carefully. Let's restructure:

# Correcting the facts based on natural language:
# "The squirrel does not see the lion" -> we should NOT assert sees('squirrel', 'lion')
# "The squirrel does not see the rabbit" -> we should NOT assert sees('squirrel', 'rabbit')

# So corrected facts:
engine.add_case_fact('facts', ('is_cold', 'lion'))
engine.add_case_fact('facts', ('visits', 'lion', 'squirrel'))

# mouse facts
engine.add_case_fact('facts', ('is_cold', 'mouse'))

# rabbit facts  
engine.add_case_fact('facts', ('is_cold', 'rabbit'))
engine.add_case_fact('facts', ('is_rough', 'rabbit'))

# squirrel facts
engine.add_case_fact('facts', ('is_kind', 'squirrel'))
engine.add_case_fact('facts', ('needs', 'squirrel', 'mouse'))
engine.add_case_fact('facts', ('needs', 'squirrel', 'rabbit'))

# Note: squirrel does NOT see lion and rabbit - so we don't assert sees for these

# --- Rules ---
@engine.rule
def mouse_see_lion_rule():
    """
    If something needs the rabbit and the rabbit sees the mouse then the mouse does not see the lion.
    """
    # But wait - we have no fact that rabbit sees mouse, so this rule won't fire
    # In PyKe, we need to express: needs(?x, rabbit) ∧ sees(rabbit, mouse) → ¬sees(mouse, lion)
    # But since we don't have sees(rabbit, mouse), this rule is not applicable
    pass  # This rule cannot fire with current facts

@engine.rule  
def rough_visits_mouse():
    """
    If something is rough then it visits the mouse.
    """
    # needs to be expressed as: is_rough(?x) → visits(?x, mouse)
    pass  # We'll use a different approach

# Actually, let's rewrite using proper PyKe syntax with facts and rules modules:

engine = knowledge_engine.engine(__file__)

# Facts
engine.add_case_fact('facts', ('is_cold', 'lion'))
engine.add_case_fact('facts', ('visits', 'lion', 'squirrel'))

engine.add_case_fact('facts', ('is_cold', 'mouse'))

engine.add_case_fact('facts', ('is_cold', 'rabbit'))
engine.add_case_fact('facts', ('is_rough', 'rabbit'))

engine.add_case_fact('facts', ('is_kind', 'squirrel'))
engine.add_case_fact('facts', ('needs', 'squirrel', 'mouse'))
engine.add_case_fact('facts', ('needs', 'squirrel', 'rabbit'))

# Note: squirrel does not see lion or rabbit - so we don't assert sees(squirrel, lion) or sees(squirrel, rabbit)

# Rules
@engine.rule
def rough_visits_mouse_rule():
    """
    If something is rough then it visits the mouse.
    """
    # In PyKe, we need to use pattern matching
    pass  # Let's use a different approach with facts and rules

# Actually, let me provide the correct PyKe syntax that will work:

engine = knowledge_engine.engine(__file__)

# Facts
engine.add_case_fact('facts', ('is_cold', 'lion'))
engine.add_case_fact('facts', ('visits', 'lion', 'squirrel'))

engine.add_case_fact('facts', ('is_cold', 'mouse'))

engine.add_case_fact('facts', ('is_cold', 'rabbit'))
engine.add_case_fact('facts', ('is_rough', 'rabbit'))

engine.add_case_fact('facts', ('is_kind', 'squirrel'))
engine.add_case_fact('facts', ('needs', 'squirrel', 'mouse'))
engine.add_case_fact('facts', ('needs', 'squirrel', 'rabbit'))

# Since squirrel does not see lion or rabbit, we need to handle negation.
# In PyKe, we can use the 'not' pattern in rules.

# Rules
@engine.rule
def rough_visits_mouse():
    """
    If something is rough then it visits the mouse.
    """
    return (
        (facts, 'is_rough', '?x'),
        facts.assert_('visits', '?x', 'mouse')
    )

@engine.rule
def needs_rabbit_and_visits_mouse_then_mouse_needs_rabbit():
    """
    If something needs the rabbit and it visits the mouse then the mouse needs the rabbit.
    """
    return (
        (facts, 'needs', '?x', 'rabbit'),
        (facts, 'visits', '?x', 'mouse'),
        facts.assert_('needs', 'mouse', 'rabbit')
    )

@engine.rule
def needs_rabbit_and_cold_rabbit_then_rough():
    """
    If something needs the rabbit and the rabbit is cold then it is rough.
    """
    return (
        (facts, 'needs', '?x', 'rabbit'),
        (facts, 'is_cold', 'rabbit'),
        facts.assert_('is_rough', '?x')
    )

@engine.rule
def needs_rabbit_then_rabbit_needs_squirrel():
    """
    If something needs the rabbit then the rabbit needs the squirrel.
    """
    return (
        (facts, 'needs', '?x', 'rabbit'),
        facts.assert_('needs', 'rabbit', 'squirrel')
    )

@engine.rule
def squirrel_sees_lion_and_not_green_then_lion_needs_squirrel():
    """
    If the squirrel sees the lion and the squirrel is not green then the lion needs the squirrel.
    """
    return (
        (facts, 'sees', 'squirrel', 'lion'),
        facts.not_(('facts', 'is_green', 'squirrel')),
        facts.assert_('needs', 'lion', 'squirrel')
    )

@engine.rule
def visits_squirrel_and_squirrel_sees_lion_then_lion_not_kind():
    """
    If something visits the squirrel and the squirrel sees the lion then the lion is not kind.
    """
    return (
        (facts, 'visits', '?x', 'squirrel'),
        (facts, 'sees', 'squirrel', 'lion'),
        facts.assert_('is_kind', 'lion', False)
    )

# Query
engine.add_case_fact('query', ('needs', 'mouse', 'rabbit'))