from pyke import knowledge_engine

engine = knowledge_engine.engine(__file__)

# --- Facts ---
engine.add_case_fact('kb', ('is_big', 'Bob'))
engine.add_case_fact('kb', ('is_cold', 'Bob'))
engine.add_case_fact('kb', ('is_furry', 'Bob'))
engine.add_case_fact('kb', ('is_smart', 'Bob'))

engine.add_case_fact('kb', ('is_cold', 'Fiona'))
engine.add_case_fact('kb', ('not_green', 'Fiona'))  # Fiona is not green
engine.add_case_fact('kb', ('is_white', 'Fiona'))

engine.add_case_fact('kb', ('is_smart', 'Gary'))

engine.add_case_fact('kb', ('is_big', 'Harry'))
engine.add_case_fact('kb', ('is_cold', 'Harry'))
engine.add_case_fact('kb', ('is_smart', 'Harry'))

# --- Rules ---
@engine.rule
def green_implies_furry(ctx, x):
    """
    All green people are furry.
    """
    if ('is_green', x) in ctx.kb:
        return [('is_furry', x)]

@engine.rule
def furry_and_not_smart_implies_white(ctx, x):
    """
    If Gary is furry and Gary is not smart then Gary is white.
    (Generalized: if someone is furry and not smart, they are white)
    """
    if ('is_furry', x) in ctx.kb and ('not_smart', x) in ctx.kb:
        return [('is_white', x)]

@engine.rule
def smart_implies_green(ctx, x):
    """
    Smart people are green.
    """
    if ('is_smart', x) in ctx.kb:
        return [('is_green', x)]

@engine.rule
def not_green_and_not_white_implies_furry(ctx, x):
    """
    If Bob is not green and Bob is not white then Bob is furry.
    (Generalized: if someone is not green and not white, they are furry)
    """
    if ('not_green', x) in ctx.kb and ('not_white', x) in ctx.kb:
        return [('is_furry', x)]

@engine.rule
def big_implies_cold(ctx, x):
    """
    Big people are cold.
    """
    if ('is_big', x) in ctx.kb:
        return [('is_cold', x)]

@engine.rule
def smart_and_furry_implies_big(ctx, x):
    """
    If someone is smart and furry then they are big.
    """
    if ('is_smart', x) in ctx.kb and ('is_furry', x) in ctx.kb:
        return [('is_big', x)]

@engine.rule
def white_and_not_cold_implies_not_blue(ctx, x):
    """
    If someone is white and not cold then they are not blue.
    """
    if ('is_white', x) in ctx.kb and ('not_cold', x) in ctx.kb:
        return [('not_blue', x)]

@engine.rule
def cold_implies_not_blue(ctx, x):
    """
    All cold people are not blue.
    """
    if ('is_cold', x) in ctx.kb:
        return [('not_blue', x)]

# --- Query ---
@engine.query
def is_bob_white(ctx):
    """
    Is Bob white?
    """
    return [('is_white', 'Bob')]

# Run the engine to activate rules
engine.activate('kb')