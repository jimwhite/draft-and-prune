from pyke import knowledge_engine

kb = knowledge_engine.engine(__file__)

# Facts
kb.add_caseless_fact('facts', 'is_smart', ('Anne', True))
kb.add_caseless_fact('facts', 'is_nice', ('Charlie', True))
kb.add_caseless_fact('facts', 'is_furry', ('Erin', True))
kb.add_caseless_fact('facts', 'is_white', ('Erin', True))
kb.add_caseless_fact('facts', 'is_smart', ('Fiona', True))
kb.add_caseless_fact('facts', 'is_white', ('Fiona', True))
kb.add_caseless_fact('facts', 'is_young', ('Fiona', True))

# Rules
@kb.rule('rules')
def young_from_nice_smart(X):
    return (kb.facts['facts', 'is_nice', (X, True)] and
            kb.facts['facts', 'is_smart', (X, True)])

@young_from_nice_smart
def young_from_nice_smart_conclusion(X):
    kb.add_caseless_fact('facts', 'is_young', (X, True))

@kb.rule('rules')
def cold_from_young_white(X):
    return (kb.facts['facts', 'is_young', (X, True)] and
            kb.facts['facts', 'is_white', (X, True)])

@cold_from_young_white
def cold_from_young_white_conclusion(X):
    kb.add_caseless_fact('facts', 'is_cold', (X, True))

@kb.rule('rules')
def red_from_white(X):
    return kb.facts['facts', 'is_white', (X, True)]

@red_from_white
def red_from_white_conclusion(X):
    kb.add_caseless_fact('facts', 'is_red', (X, True))

@kb.rule('rules')
def nice_from_furry_red(X):
    return (kb.facts['facts', 'is_furry', (X, True)] and
            kb.facts['facts', 'is_red', (X, True)])

@nice_from_furry_red
def nice_from_furry_red_conclusion(X):
    kb.add_caseless_fact('facts', 'is_nice', (X, True))

@kb.rule('rules')
def white_from_young(X):
    return kb.facts['facts', 'is_young', (X, True)]

@white_from_young
def white_from_young_conclusion(X):
    kb.add_caseless_fact('facts', 'is_white', (X, True))

@kb.rule('rules')
def furry_from_smart_cold(X):
    return (kb.facts['facts', 'is_smart', (X, True)] and
            kb.facts['facts', 'is_cold', (X, True)])

@furry_from_smart_cold
def furry_from_smart_cold_conclusion(X):
    kb.add_caseless_fact('facts', 'is_furry', (X, True))

@kb.rule('rules')
def smart_from_nice_white(X):
    return (kb.facts['facts', 'is_nice', (X, True)] and
            kb.facts['facts', 'is_white', (X, True)])

@smart_from_nice_white
def smart_from_nice_white_conclusion(X):
    kb.add_caseless_fact('facts', 'is_smart', (X, True))

@kb.rule('rules')
def anne_red():
    return (kb.facts['facts', 'is_furry', ('Anne', True)] and
            kb.facts['facts', 'is_white', ('Anne', True)])

@anne_red
def anne_red_conclusion():
    kb.add_caseless_fact('facts', 'is_red', ('Anne', True))

# Query
result = kb.query('facts', 'is_cold', ('Erin', True))
print(result)