from pyke import knowledge_engine

engine = knowledge_engine.engine(__file__)

# --- Facts ---
def is_big(entity, value):
    pass

def is_cold(entity, value):
    pass

def is_kind(entity, value):
    pass

def is_quiet(entity, value):
    pass

def is_red(entity, value):
    pass

def is_rough(entity, value):
    pass

def is_smart(entity, value):
    pass

# Explicit facts
engine.add_case_fact('facts', ('is_big', 'Charlie', True))
engine.add_case_fact('facts', ('is_cold', 'Charlie', True))
engine.add_case_fact('facts', ('is_kind', 'Charlie', True))
engine.add_case_fact('facts', ('is_quiet', 'Charlie', True))
engine.add_case_fact('facts', ('is_red', 'Charlie', True))
engine.add_case_fact('facts', ('is_rough', 'Charlie', True))
engine.add_case_fact('facts', ('is_smart', 'Charlie', True))

engine.add_case_fact('facts', ('is_kind', 'Erin', True))

engine.add_case_fact('facts', ('is_quiet', 'Fiona', True))
engine.add_case_fact('facts', ('is_rough', 'Fiona', True))

engine.add_case_fact('facts', ('is_kind', 'Harry', True))
engine.add_case_fact('facts', ('is_rough', 'Harry', True))

# --- Rules ---
@engine.rule
def kind_implies_big(entity):
    return (
        ('facts', 'is_kind', entity, True),
    ), (
        ('assert', 'is_big', entity, True),
    )

@engine.rule
def kind_and_smart_implies_rough(entity):
    return (
        ('facts', 'is_kind', entity, True),
        ('facts', 'is_smart', entity, True),
    ), (
        ('assert', 'is_rough', entity, True),
    )

@engine.rule
def red_and_quiet_implies_big(entity):
    return (
        ('facts', 'is_red', entity, True),
        ('facts', 'is_quiet', entity, True),
    ), (
        ('assert', 'is_big', entity, True),
    )

@engine.rule
def red_implies_cold(entity):
    return (
        ('facts', 'is_red', entity, True),
    ), (
        ('assert', 'is_cold', entity, True),
    )

@engine.rule
def cold_and_quiet_implies_smart(entity):
    return (
        ('facts', 'is_cold', entity, True),
        ('facts', 'is_quiet', entity, True),
    ), (
        ('assert', 'is_smart', entity, True),
    )

@engine.rule
def big_and_smart_implies_cold(entity):
    return (
        ('facts', 'is_big', entity, True),
        ('facts', 'is_smart', entity, True),
    ), (
        ('assert', 'is_cold', entity, True),
    )

@engine.rule
def quiet_implies_cold(entity):
    return (
        ('facts', 'is_quiet', entity, True),
    ), (
        ('assert', 'is_cold', entity, True),
    )

@engine.rule
def kind_and_big_implies_red(entity):
    return (
        ('facts', 'is_kind', entity, True),
        ('facts', 'is_big', entity, True),
    ), (
        ('assert', 'is_red', entity, True),
    )

@engine.rule
def cold_and_smart_implies_kind(entity):
    return (
        ('facts', 'is_cold', entity, True),
        ('facts', 'is_smart', entity, True),
    ), (
        ('assert', 'is_kind', entity, True),
    )

# --- Query ---
def query_fiona_not_red():
    # Try to prove that Fiona is not red
    try:
        # First check if we can prove Fiona IS red
        engine.prove(('facts', 'is_red', 'Fiona', True), 1)
        return False  # If proven red, then "not red" is false
    except:
        try:
            # Check if we can prove Fiona is NOT red (using negation as failure)
            engine.prove(('not', ('facts', 'is_red', 'Fiona', True)), 1)
            return True  # If proven not red, then statement is true
        except:
            return None  # Unknown

# Run the query
result = query_fiona_not_red()
print(result)