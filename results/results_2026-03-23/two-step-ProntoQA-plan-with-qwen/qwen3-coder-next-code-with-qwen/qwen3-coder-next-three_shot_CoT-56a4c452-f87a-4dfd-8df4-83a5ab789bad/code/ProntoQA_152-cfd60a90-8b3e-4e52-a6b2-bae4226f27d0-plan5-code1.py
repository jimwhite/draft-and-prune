from pyke import knowledge_engine, facts, rules

# Initialize knowledge engine
engine = knowledge_engine.engine(__name__)

# Facts
engine.add_case_fact('facts', ('is_a', 'Wren', 'yumpus', True))

# Rules
@rules.rule(
    '$thing',
    facts.is_a('$thing', 'jompus', True),
    None,
    facts.is_bright('$thing', True)
)
def jompus_is_bright():
    pass

@rules.rule(
    '$thing',
    facts.is_a('$thing', 'jompus', True),
    None,
    facts.is_a('$thing', 'vumpus', True)
)
def jompus_is_vumpus():
    pass

@rules.rule(
    '$thing',
    facts.is_a('$thing', 'vumpus', True),
    None,
    facts.is_floral('$thing', True)
)
def vumpus_is_floral():
    pass

@rules.rule(
    '$thing',
    facts.is_a('$thing', 'vumpus', True),
    None,
    facts.is_a('$thing', 'yumpus', True)
)
def vumpus_is_yumpus():
    pass

@rules.rule(
    '$thing',
    facts.is_a('$thing', 'yumpus', True),
    None,
    facts.is_temperate('$thing', False)
)
def yumpus_is_not_temperate():
    pass

@rules.rule(
    '$thing',
    facts.is_a('$thing', 'yumpus', True),
    None,
    facts.is_a('$thing', 'numpus', True)
)
def yumpus_is_numpus():
    pass

@rules.rule(
    '$thing',
    facts.is_a('$thing', 'numpus', True),
    None,
    facts.is_sweet('$thing', True)
)
def numpus_is_sweet():
    pass

@rules.rule(
    '$thing',
    facts.is_a('$thing', 'numpus', True),
    None,
    facts.is_a('$thing', 'zumpus', True)
)
def numpus_is_zumpus():
    pass

@rules.rule(
    '$thing',
    facts.is_a('$thing', 'zumpus', True),
    None,
    facts.is_mean('$thing', True)
)
def zumpus_is_mean():
    pass

@rules.rule(
    '$thing',
    facts.is_a('$thing', 'zumpus', True),
    None,
    facts.is_a('$thing', 'rompus', True)
)
def zumpus_is_rompus():
    pass

@rules.rule(
    '$thing',
    facts.is_a('$thing', 'rompus', True),
    None,
    facts.is_feisty('$thing', False)
)
def rompus_is_not_feisty():
    pass

@rules.rule(
    '$thing',
    facts.is_a('$thing', 'impus', True),
    None,
    facts.is_transparent('$thing', False)
)
def impus_is_not_transparent():
    pass

@rules.rule(
    '$thing',
    facts.is_a('$thing', 'rompus', True),
    None,
    facts.is_a('$thing', 'wumpus', True)
)
def rompus_is_wumpus():
    pass

@rules.rule(
    '$thing',
    facts.is_a('$thing', 'wumpus', True),
    None,
    facts.is_transparent('$thing', True)
)
def wumpus_is_transparent():
    pass

@rules.rule(
    '$thing',
    facts.is_a('$thing', 'wumpus', True),
    None,
    facts.is_a('$thing', 'dumpus', True)
)
def wumpus_is_dumpus():
    pass

@rules.rule(
    '$thing',
    facts.is_a('$thing', 'dumpus', True),
    None,
    facts.is_large('$thing', True)
)
def dumpus_is_large():
    pass

@rules.rule(
    '$thing',
    facts.is_a('$thing', 'dumpus', True),
    None,
    facts.is_a('$thing', 'tumpus', True)
)
def dumpus_is_tumpus():
    pass

# Activate the knowledge base
engine.activate('rules')

# Query
result = engine.query(facts.is_transparent('Wren', True))
print("True" if result else "False")