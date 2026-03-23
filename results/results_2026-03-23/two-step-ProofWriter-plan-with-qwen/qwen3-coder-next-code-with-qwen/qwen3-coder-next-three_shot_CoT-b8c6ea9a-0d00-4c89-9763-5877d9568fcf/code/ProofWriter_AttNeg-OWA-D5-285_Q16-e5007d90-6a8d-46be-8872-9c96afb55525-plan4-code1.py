from pyke import knowledge_engine

# Create knowledge engine instance
engine = knowledge_engine.engine(__file__)

# --- Facts ---
engine.add_casefact('kb', 'is_big', ('Bob', True))
engine.add_casefact('kb', 'is_cold', ('Bob', True))
engine.add_casefact('kb', 'is_furry', ('Bob', True))
engine.add_casefact('kb', 'is_smart', ('Bob', True))

engine.add_casefact('kb', 'is_cold', ('Fiona', True))
engine.add_casefact('kb', 'is_green', ('Fiona', False))  # Fiona is not green
engine.add_casefact('kb', 'is_white', ('Fiona', True))

engine.add_casefact('kb', 'is_smart', ('Gary', True))

engine.add_casefact('kb', 'is_big', ('Harry', True))
engine.add_casefact('kb', 'is_cold', ('Harry', True))
engine.add_casefact('kb', 'is_smart', ('Harry', True))

# --- Rules ---
@engine.rule
def green_implies_furry(ctx, x):
    """
    All green people are furry.
    """
    if ctx.kb.is_green(x, True):
        return [('is_furry', (x, True))]

@engine.rule
def furry_and_not_smart_implies_white(ctx, x):
    """
    If Gary is furry and Gary is not smart then Gary is white.
    (Generalized: if someone is furry and not smart, they are white)
    """
    if ctx.kb.is_furry(x, True) and not ctx.kb.is_smart(x, True):
        return [('is_white', (x, True))]

@engine.rule
def smart_implies_green(ctx, x):
    """
    Smart people are green.
    """
    if ctx.kb.is_smart(x, True):
        return [('is_green', (x, True))]

@engine.rule
def bob_not_green_and_not_white_implies_furry(ctx):
    """
    If Bob is not green and Bob is not white then Bob is furry.
    """
    if (not ctx.kb.is_green('Bob', True) and 
        not ctx.kb.is_white('Bob', True)):
        return [('is_furry', ('Bob', True))]

@engine.rule
def big_implies_cold(ctx, x):
    """
    Big people are cold.
    """
    if ctx.kb.is_big(x, True):
        return [('is_cold', (x, True))]

@engine.rule
def smart_and_furry_implies_big(ctx, x):
    """
    If someone is smart and furry then they are big.
    """
    if ctx.kb.is_smart(x, True) and ctx.kb.is_furry(x, True):
        return [('is_big', (x, True))]

@engine.rule
def white_and_not_cold_implies_not_blue(ctx, x):
    """
    If someone is white and not cold then they are not blue.
    """
    if ctx.kb.is_white(x, True) and not ctx.kb.is_cold(x, True):
        return [('is_blue', (x, False))]

@engine.rule
def cold_implies_not_blue(ctx, x):
    """
    All cold people are not blue.
    """
    if ctx.kb.is_cold(x, True):
        return [('is_blue', (x, False))]

# --- Query ---
def check_bob_white():
    return engine.kb.is_white('Bob', True)

# Execute and get result
if __name__ == "__main__":
    engine.activate('kb')
    
    # Try to prove Bob is white
    try:
        result = check_bob_white()
        print("Bob is white:", result)
    except Exception as e:
        # If we can't prove it, check if we can prove he's not white
        try:
            not_result = engine.kb.is_white('Bob', False)
            print("Bob is white:", not not_result)
        except:
            print("Unknown")