# Import required PyKe modules
from pyke import knowledge_engine

# Create knowledge engine instance
engine = knowledge_engine.engine(__file__)

# --- Facts ---
engine.add_casefact('kb', 'is_big', ('Bob', True))
engine.add_casefact('kb', 'is_cold', ('Bob', True))
engine.add_casefact('kb', 'is_furry', ('Bob', True))
engine.add_casefact('kb', 'is_smart', ('Bob', True))

engine.add_casefact('kb', 'is_cold', ('Fiona', True))
engine.add_casefact('kb', 'is_green', ('Fiona', False))
engine.add_casefact('kb', 'is_white', ('Fiona', True))

engine.add_casefact('kb', 'is_smart', ('Gary', True))

engine.add_casefact('kb', 'is_big', ('Harry', True))
engine.add_casefact('kb', 'is_cold', ('Harry', True))
engine.add_casefact('kb', 'is_smart', ('Harry', True))

# --- Rules ---
@engine.rule
def green_implies_furry(kb, x):
    """
    All green people are furry.
    """
    if kb.is_green(x, True):
        return [('furry', x, True)]

@engine.rule
def furry_and_not_smart_implies_white(kb, x):
    """
    If Gary is furry and Gary is not smart then Gary is white.
    (Generalized: if someone is furry and not smart, they are white)
    """
    if kb.is_furry(x, True) and not kb.is_smart(x, True):
        return [('white', x, True)]

@engine.rule
def smart_implies_green(kb, x):
    """
    Smart people are green.
    """
    if kb.is_smart(x, True):
        return [('green', x, True)]

@engine.rule
def not_green_and_not_white_implies_furry(kb, x):
    """
    If Bob is not green and Bob is not white then Bob is furry.
    (Generalized: if someone is not green and not white, they are furry)
    """
    if not kb.is_green(x, True) and not kb.is_white(x, True):
        return [('furry', x, True)]

@engine.rule
def big_implies_cold(kb, x):
    """
    Big people are cold.
    """
    if kb.is_big(x, True):
        return [('cold', x, True)]

@engine.rule
def smart_and_furry_implies_big(kb, x):
    """
    If someone is smart and furry then they are big.
    """
    if kb.is_smart(x, True) and kb.is_furry(x, True):
        return [('big', x, True)]

@engine.rule
def white_and_not_cold_implies_not_blue(kb, x):
    """
    If someone is white and not cold then they are not blue.
    """
    if kb.is_white(x, True) and not kb.is_cold(x, True):
        return [('not_blue', x, True)]

@engine.rule
def cold_implies_not_blue(kb, x):
    """
    All cold people are not blue.
    """
    if kb.is_cold(x, True):
        return [('not_blue', x, True)]

# --- Query ---
def query_bob_white():
    # Initialize the engine
    engine.activate('kb')
    
    # Check if Bob is white
    result = list(engine.prove_1('kb', 'is_white', ('Bob', True), 1))
    return len(result) > 0

# Execute query
is_bob_white = query_bob_white()
print(f"Bob is white: {is_bob_white}")