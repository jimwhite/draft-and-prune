import pyke

# Initialize knowledge engine
engine = pyke.knowledge_engine.engine()

# Facts section
engine.add_facts('''
Facts:
is_a(Wren, tumpus, True)
''')

# Rules section
engine.add_rules('''
Rules:
wumpus_is_sour:
    is_a($thing, wumpus, True)
    =>
    is_sour($thing, True)

wumpus_is_yumpus:
    is_a($thing, wumpus, True)
    =>
    is_a($thing, yumpus, True)

yumpus_is_aggressive:
    is_a($thing, yumpus, True)
    =>
    is_aggressive($thing, True)

yumpus_is_tumpus:
    is_a($thing, yumpus, True)
    =>
    is_a($thing, tumpus, True)

tumpus_is_transparent:
    is_a($thing, tumpus, True)
    =>
    is_transparent($thing, True)

tumpus_is_vumpus:
    is_a($thing, tumpus, True)
    =>
    is_a($thing, vumpus, True)

vumpus_is_wooden:
    is_a($thing, vumpus, True)
    =>
    is_wooden($thing, True)

vumpus_is_jompus:
    is_a($thing, vumpus, True)
    =>
    is_a($thing, jompus, True)

impus_is_not_feisty:
    is_a($thing, impus, True)
    =>
    is_feisty($thing, False)

jompus_is_large:
    is_a($thing, jompus, True)
    =>
    is_large($thing, True)

jompus_is_numpus:
    is_a($thing, jompus, True)
    =>
    is_a($thing, numpus, True)

numpus_is_red:
    is_a($thing, numpus, True)
    =>
    is_red($thing, True)

numpus_is_rompus:
    is_a($thing, numpus, True)
    =>
    is_a($thing, rompus, True)

rompus_is_feisty:
    is_a($thing, rompus, True)
    =>
    is_feisty($thing, True)

rompus_is_zumpus:
    is_a($thing, rompus, True)
    =>
    is_a($thing, zumpus, True)
''')

# Run the engine to apply all rules
engine.activate('rules')  # Activate the rule set

# Query section - check if Wren is feisty
result = engine.query(('is_feisty', 'Wren', True))

# Output the result for "Wren is not feisty" (which is the negation)
print(not result)