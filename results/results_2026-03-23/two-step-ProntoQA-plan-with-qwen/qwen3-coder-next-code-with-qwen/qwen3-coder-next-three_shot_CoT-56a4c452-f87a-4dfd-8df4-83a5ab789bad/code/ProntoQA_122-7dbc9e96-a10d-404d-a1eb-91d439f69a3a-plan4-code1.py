from pyke import knowledge_engine, facts, rules

# Initialize knowledge engine
engine = knowledge_engine.engine('')

# Facts
engine.facts.add('is_a', 'Fae', 'numpus', True)

# Rules
@rule(
    foreach=facts.is_a('?', 'rompus', True),
    then=lambda ce, thing: facts.is_metallic(thing, True)
)
def rompus_is_metallic(ce):
    pass

@rule(
    foreach=facts.is_a('?', 'rompus', True),
    then=lambda ce, thing: facts.is_a(thing, 'dumpus', True)
)
def rompus_is_dumpus(ce):
    pass

@rule(
    foreach=facts.is_a('?', 'dumpus', True),
    then=lambda ce, thing: facts.is_blue(thing, True)
)
def dumpus_is_blue(ce):
    pass

@rule(
    foreach=facts.is_a('?', 'dumpus', True),
    then=lambda ce, thing: facts.is_a(thing, 'numpus', True)
)
def dumpus_is_numpus(ce):
    pass

@rule(
    foreach=facts.is_a('?', 'numpus', True),
    then=lambda ce, thing: facts.is_fruity(thing, True)
)
def numpus_is_fruity(ce):
    pass

@rule(
    foreach=facts.is_a('?', 'numpus', True),
    then=lambda ce, thing: facts.is_a(thing, 'jompus', True)
)
def numpus_is_jompus(ce):
    pass

@rule(
    foreach=facts.is_a('?', 'jompus', True),
    then=lambda ce, thing: facts.is_mean(thing, True)
)
def jompus_is_mean(ce):
    pass

@rule(
    foreach=facts.is_a('?', 'jompus', True),
    then=lambda ce, thing: facts.is_a(thing, 'tumpus', True)
)
def jompus_is_tumpus(ce):
    pass

@rule(
    foreach=facts.is_a('?', 'tumpus', True),
    then=lambda ce, thing: facts.is_temperate(thing, False)
)
def tumpus_is_not_temperate(ce):
    pass

@rule(
    foreach=facts.is_a('?', 'tumpus', True),
    then=lambda ce, thing: facts.is_a(thing, 'impus', True)
)
def tumpus_is_impus(ce):
    pass

@rule(
    foreach=facts.is_a('?', 'impus', True),
    then=lambda ce, thing: facts.is_dull(thing, False)
)
def impus_is_not_dull(ce):
    pass

@rule(
    foreach=facts.is_a('?', 'impus', True),
    then=lambda ce, thing: facts.is_a(thing, 'yumpus', True)
)
def impus_is_yumpus(ce):
    pass

@rule(
    foreach=facts.is_a('?', 'yumpus', True),
    then=lambda ce, thing: facts.is_transparent(thing, False)
)
def yumpus_is_not_transparent(ce):
    pass

@rule(
    foreach=facts.is_a('?', 'yumpus', True),
    then=lambda ce, thing: facts.is_a(thing, 'zumpus', True)
)
def yumpus_is_zumpus(ce):
    pass

@rule(
    foreach=facts.is_a('?', 'wumpus', True),
    then=lambda ce, thing: facts.is_transparent(thing, True)
)
def wumpus_is_transparent(ce):
    pass

@rule(
    foreach=facts.is_a('?', 'zumpus', True),
    then=lambda ce, thing: facts.is_sweet(thing, False)
)
def zumpus_is_not_sweet(ce):
    pass

@rule(
    foreach=facts.is_a('?', 'zumpus', True),
    then=lambda ce, thing: facts.is_a(thing, 'vumpus', True)
)
def zumpus_is_vumpus(ce):
    pass

# Query
result = engine.facts.is_transparent('Fae', True)