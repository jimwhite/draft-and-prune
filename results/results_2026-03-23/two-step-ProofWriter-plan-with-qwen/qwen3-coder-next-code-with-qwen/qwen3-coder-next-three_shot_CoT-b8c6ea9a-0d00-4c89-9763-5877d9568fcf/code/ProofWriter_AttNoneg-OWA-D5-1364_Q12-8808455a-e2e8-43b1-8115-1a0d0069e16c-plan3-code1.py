from pyke import knowledge_engine

engine = knowledge_engine.engine(__file__)

# --- Facts ---
def is_big(entity, value):
    return engine.get_kb('facts').is_big.assert_(entity, value)

def is_cold(entity, value):
    return engine.get_kb('facts').is_cold.assert_(entity, value)

def is_kind(entity, value):
    return engine.get_kb('facts').is_kind.assert_(entity, value)

def is_quiet(entity, value):
    return engine.get_kb('facts').is_quiet.assert_(entity, value)

def is_red(entity, value):
    return engine.get_kb('facts').is_red.assert_(entity, value)

def is_rough(entity, value):
    return engine.get_kb('facts').is_rough.assert_(entity, value)

def is_smart(entity, value):
    return engine.get_kb('facts').is_smart.assert_(entity, value)

# Assert all facts
engine.get_kb('facts').is_big.add(('Charlie', True))
engine.get_kb('facts').is_cold.add(('Charlie', True))
engine.get_kb('facts').is_kind.add(('Charlie', True))
engine.get_kb('facts').is_quiet.add(('Charlie', True))
engine.get_kb('facts').is_red.add(('Charlie', True))
engine.get_kb('facts').is_rough.add(('Charlie', True))
engine.get_kb('facts').is_smart.add(('Charlie', True))

engine.get_kb('facts').is_kind.add(('Erin', True))

engine.get_kb('facts').is_quiet.add(('Fiona', True))
engine.get_kb('facts').is_rough.add(('Fiona', True))

engine.get_kb('facts').is_kind.add(('Harry', True))
engine.get_kb('facts').is_rough.add(('Harry', True))

# --- Rules ---
@engine.rule
def kind_implies_big():
    """
    foreach ?x is kind(?x, True)
    => assert(is_big(?x, True))
    """
    for x in engine.get_kb('facts').is_kind.query():
        if x[1] is True:
            engine.get_kb('facts').is_big.assert_((x[0], True))

@engine.rule
def kind_and_smart_implies_rough():
    """
    foreach ?x is kind(?x, True), ?x is smart(?x, True)
    => assert(is_rough(?x, True))
    """
    for x in engine.get_kb('facts').is_kind.query():
        if x[1] is True:
            for y in engine.get_kb('facts').is_smart.query():
                if y[1] is True and x[0] == y[0]:
                    engine.get_kb('facts').is_rough.assert_((x[0], True))

@engine.rule
def red_and_quiet_implies_big():
    """
    foreach ?x is red(?x, True), ?x is quiet(?x, True)
    => assert(is_big(?x, True))
    """
    for x in engine.get_kb('facts').is_red.query():
        if x[1] is True:
            for y in engine.get_kb('facts').is_quiet.query():
                if y[1] is True and x[0] == y[0]:
                    engine.get_kb('facts').is_big.assert_((x[0], True))

@engine.rule
def red_implies_cold():
    """
    foreach ?x is red(?x, True)
    => assert(is_cold(?x, True))
    """
    for x in engine.get_kb('facts').is_red.query():
        if x[1] is True:
            engine.get_kb('facts').is_cold.assert_((x[0], True))

@engine.rule
def cold_and_quiet_implies_smart():
    """
    foreach ?x is cold(?x, True), ?x is quiet(?x, True)
    => assert(is_smart(?x, True))
    """
    for x in engine.get_kb('facts').is_cold.query():
        if x[1] is True:
            for y in engine.get_kb('facts').is_quiet.query():
                if y[1] is True and x[0] == y[0]:
                    engine.get_kb('facts').is_smart.assert_((x[0], True))

@engine.rule
def big_and_smart_implies_cold():
    """
    foreach ?x is big(?x, True), ?x is smart(?x, True)
    => assert(is_cold(?x, True))
    """
    for x in engine.get_kb('facts').is_big.query():
        if x[1] is True:
            for y in engine.get_kb('facts').is_smart.query():
                if y[1] is True and x[0] == y[0]:
                    engine.get_kb('facts').is_cold.assert_((x[0], True))

@engine.rule
def quiet_implies_cold():
    """
    foreach ?x is quiet(?x, True)
    => assert(is_cold(?x, True))
    """
    for x in engine.get_kb('facts').is_quiet.query():
        if x[1] is True:
            engine.get_kb('facts').is_cold.assert_((x[0], True))

@engine.rule
def kind_and_big_implies_red():
    """
    foreach ?x is kind(?x, True), ?x is big(?x, True)
    => assert(is_red(?x, True))
    """
    for x in engine.get_kb('facts').is_kind.query():
        if x[1] is True:
            for y in engine.get_kb('facts').is_big.query():
                if y[1] is True and x[0] == y[0]:
                    engine.get_kb('facts').is_red.assert_((x[0], True))

@engine.rule
def cold_and_smart_implies_kind():
    """
    foreach ?x is cold(?x, True), ?x is smart(?x, True)
    => assert(is_kind(?x, True))
    """
    for x in engine.get_kb('facts').is_cold.query():
        if x[1] is True:
            for y in engine.get_kb('facts').is_smart.query():
                if y[1] is True and x[0] == y[0]:
                    engine.get_kb('facts').is_kind.assert_((x[0], True))

# --- Query ---
def query_fiona_not_red():
    """
    Check if Fiona is not red
    """
    # First, run forward chaining to apply all rules
    engine.activate('facts')
    
    # Check if Fiona is red
    result = list(engine.get_kb('facts').is_red.query())
    
    # Fiona is not red if ('Fiona', True) is not in the results
    fiona_red = any(item[0] == 'Fiona' and item[1] is True for item in result)
    
    return not fiona_red

# Execute and get result
if __name__ == "__main__":
    engine.activate('facts')
    is_fiona_not_red = query_fiona_not_red()
    print(f"Fiona is not red: {is_fiona_not_red}")