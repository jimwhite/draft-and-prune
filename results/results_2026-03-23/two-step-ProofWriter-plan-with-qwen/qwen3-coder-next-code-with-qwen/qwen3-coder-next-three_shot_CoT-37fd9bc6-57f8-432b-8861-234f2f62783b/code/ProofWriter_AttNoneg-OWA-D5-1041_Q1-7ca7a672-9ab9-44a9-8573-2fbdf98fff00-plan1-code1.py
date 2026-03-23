from pyke import knowledge_engine

# Create knowledge engine instance
engine = knowledge_engine.engine(__file__)

# --- Facts ---
engine.add_casefact(('facts', 'is_cold'), ('Bob', True))
engine.add_casefact(('facts', 'is_quiet'), ('Bob', True))
engine.add_casefact(('facts', 'is_red'), ('Bob', True))
engine.add_casefact(('facts', 'is_smart'), ('Bob', True))

engine.add_casefact(('facts', 'is_kind'), ('Charlie', True))
engine.add_casefact(('facts', 'is_quiet'), ('Charlie', True))
engine.add_casefact(('facts', 'is_red'), ('Charlie', True))
engine.add_casefact(('facts', 'is_rough'), ('Charlie', True))

engine.add_casefact(('facts', 'is_cold'), ('Dave', True))
engine.add_casefact(('facts', 'is_kind'), ('Dave', True))
engine.add_casefact(('facts', 'is_smart'), ('Dave', True))

engine.add_casefact(('facts', 'is_quiet'), ('Fiona', True))

# --- Rules ---
@engine.rule
def smart_from_cold_quiet(kb, x):
    """
    If something is quiet and cold then it is smart.
    """
    if kb.facts.is_quiet(x, True) and kb.facts.is_cold(x, True):
        return [('is_smart', x, True)]

@engine.rule
def round_from_red_cold(kb, x):
    """
    Red, cold things are round.
    """
    if kb.facts.is_red(x, True) and kb.facts.is_cold(x, True):
        return [('is_round', x, True)]

@engine.rule
def red_from_kind_rough(kb, x):
    """
    If something is kind and rough then it is red.
    """
    if kb.facts.is_kind(x, True) and kb.facts.is_rough(x, True):
        return [('is_red', x, True)]

@engine.rule
def rough_from_quiet(kb, x):
    """
    All quiet things are rough.
    """
    if kb.facts.is_quiet(x, True):
        return [('is_rough', x, True)]

@engine.rule
def red_from_cold_smart(kb, x):
    """
    Cold, smart things are red.
    """
    if kb.facts.is_cold(x, True) and kb.facts.is_smart(x, True):
        return [('is_red', x, True)]

@engine.rule
def cold_from_rough(kb, x):
    """
    If something is rough then it is cold.
    """
    if kb.facts.is_rough(x, True):
        return [('is_cold', x, True)]

@engine.rule
def rough_from_red(kb, x):
    """
    All red things are rough.
    """
    if kb.facts.is_red(x, True):
        return [('is_rough', x, True)]

@engine.rule
def dave_quiet_from_smart_kind(kb):
    """
    If Dave is smart and Dave is kind then Dave is quiet.
    """
    if kb.facts.is_smart('Dave', True) and kb.facts.is_kind('Dave', True):
        return [('is_quiet', 'Dave', True)]

# --- Query ---
def check_charlie_kind():
    engine.activate('smart_from_cold_quiet')
    engine.activate('round_from_red_cold')
    engine.activate('red_from_kind_rough')
    engine.activate('rough_from_quiet')
    engine.activate('red_from_cold_smart')
    engine.activate('cold_from_rough')
    engine.activate('rough_from_red')
    engine.activate('dave_quiet_from_smart_kind')
    
    # Check if Charlie is kind
    result = engine.query.facts.is_kind('Charlie', True)
    return bool(result)

# Execute and get result
result = check_charlie_kind()
print("Charlie is kind:", result)