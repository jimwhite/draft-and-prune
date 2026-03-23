from pyke import knowledge_engine

# --- Facts ---
def add_facts(kb):
    kb.add_fact('chases', 'bald_eagle', 'mouse')
    kb.add_fact('chases', 'bald_eagle', 'squirrel')
    kb.add_fact('is_cold', 'bald_eagle')
    
    kb.add_fact('chases', 'lion', 'bald_eagle')
    # chases("lion", "mouse", False) - we only add positive facts
    kb.add_fact('chases', 'lion', 'squirrel')
    kb.add_fact('is_blue', 'lion')
    kb.add_fact('needs', 'lion', 'squirrel')
    kb.add_fact('visits', 'lion', 'squirrel')
    
    # visits("mouse", "bald_eagle", False) - we only add positive facts
    # visits("mouse", "squirrel", False) - we only add positive facts
    
    kb.add_fact('is_cold', 'squirrel')
    kb.add_fact('is_red', 'squirrel')
    # visits("squirrel", "lion", False) - we only add positive facts

# --- Rules ---
@rule(
    'chases',
    ('mouse', '?x'),
    ('is_green', 'mouse')
)
def mouse_green_if_visited(kb, x):
    # If something visits the mouse then the mouse is green.
    pass  # This rule would need visiting facts, but we don't have any

@rule(
    'chases',
    ('mouse', 'lion'),
    ('needs', 'mouse', 'lion')
)
def mouse_needs_lion_if_not_chasing(kb):
    # If the mouse does not chase the lion then the mouse needs the lion.
    pass  # We need to check if chases('mouse', 'lion') is false

@rule(
    'visits',
    ('?x', 'squirrel'),
    'chases',
    ('squirrel', 'lion'),
    ('is_green', 'lion')
)
def lion_green_if_visits_squirrel_and_squirrel_not_chasing_lion(kb, x):
    # If something visits the squirrel and the squirrel does not chase the lion then the lion is green.
    pass

@rule(
    'is_young',
    ('?x',),
    'visits',
    ('?x', 'bald_eagle')
)
def young_visits_bald_eagle(kb, x):
    # If something is young then it visits the bald eagle.
    pass

@rule(
    'visits',
    ('bald_eagle', 'squirrel'),
    ('?x', 'bald_eagle')
)
def visits_bald_eagle_then_bald_eagle_visits_squirrel(kb, x):
    # If something visits the bald eagle then the bald eagle visits the squirrel.
    pass

@rule(
    'visits',
    ('?x', 'squirrel'),
    'is_red',
    ('squirrel',),
    'is_young',
    ('?x',)
)
def visits_squirrel_and_red_then_young(kb, x):
    # If something visits the squirrel and the squirrel is red then it is young.
    pass

@rule(
    'needs',
    ('?x', 'squirrel'),
    'is_cold',
    ('?x',),
    'chases',
    ('squirrel', 'bald_eagle')
)
def needs_squirrel_and_not_cold_then_squirrel_chases_bald_eagle(kb, x):
    # If something needs the squirrel and it is not cold then the squirrel chases the bald eagle.
    pass

# --- Query ---
def query(kb):
    return kb.query('is_young', 'bald_eagle')

# Initialize knowledge engine
engine = knowledge_engine.engine(__file__)
engine.add_kb(__name__, 'kb')
add_facts(engine.kb[__name__])
# Add rules to engine
engine.activate('kb')
result = query(engine.kb[__name__])
print(result)