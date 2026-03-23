from pyke import knowledge_engine

# Create knowledge engine instance
engine = knowledge_engine.engine(__file__)

# --- Facts ---
def is_big(entity, value):
    return engine.get_kb('facts').assertz(f'is_big({entity}, {value})')

def is_cold(entity, value):
    return engine.get_kb('facts').assertz(f'is_cold({entity}, {value})')

def is_kind(entity, value):
    return engine.get_kb('facts').assertz(f'is_kind({entity}, {value})')

def is_quiet(entity, value):
    return engine.get_kb('facts').assertz(f'is_quiet({entity}, {value})')

def is_red(entity, value):
    return engine.get_kb('facts').assertz(f'is_red({entity}, {value})')

def is_rough(entity, value):
    return engine.get_kb('facts').assertz(f'is_rough({entity}, {value})')

def is_smart(entity, value):
    return engine.get_kb('facts').assertz(f'is_smart({entity}, {value})')

# Assert all facts
engine.get_kb('facts').assertz('is_big(Charlie, True)')
engine.get_kb('facts').assertz('is_cold(Charlie, True)')
engine.get_kb('facts').assertz('is_kind(Charlie, True)')
engine.get_kb('facts').assertz('is_quiet(Charlie, True)')
engine.get_kb('facts').assertz('is_red(Charlie, True)')
engine.get_kb('facts').assertz('is_rough(Charlie, True)')
engine.get_kb('facts').assertz('is_smart(Charlie, True)')

engine.get_kb('facts').assertz('is_kind(Erin, True)')

engine.get_kb('facts').assertz('is_quiet(Fiona, True)')
engine.get_kb('facts').assertz('is_rough(Fiona, True)')

engine.get_kb('facts').assertz('is_kind(Harry, True)')
engine.get_kb('facts').assertz('is_rough(Harry, True)')

# --- Rules ---
@engine.rule
def kind_implies_big():
    """
    foreach ?x is kind(?x, True) => assert(is_big(?x, True))
    """
    for x in engine.get_kb('facts').query('is_kind(?, True)'):
        yield 'is_big({0}, True)'.format(x[0])

@engine.rule
def kind_and_smart_implies_rough():
    """
    foreach ?x is kind(?x, True), ?x is smart(?x, True) => assert(is_rough(?x, True))
    """
    for x in engine.get_kb('facts').query('is_kind(?, True)'):
        if engine.get_kb('facts').query('is_smart({0}, True)'.format(x[0])):
            yield 'is_rough({0}, True)'.format(x[0])

@engine.rule
def red_and_quiet_implies_big():
    """
    foreach ?x is red(?x, True), ?x is quiet(?x, True) => assert(is_big(?x, True))
    """
    for x in engine.get_kb('facts').query('is_red(?, True)'):
        if engine.get_kb('facts').query('is_quiet({0}, True)'.format(x[0])):
            yield 'is_big({0}, True)'.format(x[0])

@engine.rule
def red_implies_cold():
    """
    foreach ?x is red(?x, True) => assert(is_cold(?x, True))
    """
    for x in engine.get_kb('facts').query('is_red(?, True)'):
        yield 'is_cold({0}, True)'.format(x[0])

@engine.rule
def cold_and_quiet_implies_smart():
    """
    foreach ?x is cold(?x, True), ?x is quiet(?x, True) => assert(is_smart(?x, True))
    """
    for x in engine.get_kb('facts').query('is_cold(?, True)'):
        if engine.get_kb('facts').query('is_quiet({0}, True)'.format(x[0])):
            yield 'is_smart({0}, True)'.format(x[0])

@engine.rule
def big_and_smart_implies_cold():
    """
    foreach ?x is big(?x, True), ?x is smart(?x, True) => assert(is_cold(?x, True))
    """
    for x in engine.get_kb('facts').query('is_big(?, True)'):
        if engine.get_kb('facts').query('is_smart({0}, True)'.format(x[0])):
            yield 'is_cold({0}, True)'.format(x[0])

@engine.rule
def quiet_implies_cold():
    """
    foreach ?x is quiet(?x, True) => assert(is_cold(?x, True))
    """
    for x in engine.get_kb('facts').query('is_quiet(?, True)'):
        yield 'is_cold({0}, True)'.format(x[0])

@engine.rule
def kind_and_big_implies_red():
    """
    foreach ?x is kind(?x, True), ?x is big(?x, True) => assert(is_red(?x, True))
    """
    for x in engine.get_kb('facts').query('is_kind(?, True)'):
        if engine.get_kb('facts').query('is_big({0}, True)'.format(x[0])):
            yield 'is_red({0}, True)'.format(x[0])

@engine.rule
def cold_and_smart_implies_kind():
    """
    foreach ?x is cold(?x, True), ?x is smart(?x, True) => assert(is_kind(?x, True))
    """
    for x in engine.get_kb('facts').query('is_cold(?, True)'):
        if engine.get_kb('facts').query('is_smart({0}, True)'.format(x[0])):
            yield 'is_kind({0}, True)'.format(x[0])

# --- Query ---
def query_fiona_not_red():
    """
    Check if Fiona is not red (i.e., is_red("Fiona", True) should be false)
    """
    result = engine.get_kb('facts').query('is_red(Fiona, True)')
    return not bool(result)

# Run the engine to apply all rules
engine.activate('rules')

# Execute query
result = query_fiona_not_red()
print(result)