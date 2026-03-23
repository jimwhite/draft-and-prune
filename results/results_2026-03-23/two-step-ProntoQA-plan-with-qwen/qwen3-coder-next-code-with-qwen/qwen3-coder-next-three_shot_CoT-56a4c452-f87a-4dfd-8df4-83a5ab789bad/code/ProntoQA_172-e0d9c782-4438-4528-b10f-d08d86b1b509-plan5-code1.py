from pyke import knowledge_engine

engine = knowledge_engine.engine(__file__)

# Facts - Rex is a zumpus
engine.add_universal_fact('is_a', 'Rex', 'zumpus')

# Rules
engine.add_rule(
    ('is_a', '$x', 'vumpus'),
    (('is_a', '$x', 'zumpus'),)
)

engine.add_rule(
    ('is_a', '$x', 'dumpus'),
    (('is_a', '$x', 'vumpus'),)
)

engine.add_rule(
    ('is_a', '$x', 'wumpus'),
    (('is_a', '$x', 'dumpus'),)
)

engine.add_rule(
    ('is_a', '$x', 'rompus'),
    (('is_a', '$x', 'wumpus'),)
)

engine.add_rule(
    ('is_opaque', '$x'),
    (('is_a', '$x', 'rompus'),)
)

# Add the negation facts as rules (zumpus is not temperate, tumpuses are not opaque)
engine.add_rule(
    ('not', ('is_temperate', '$x')),
    (('is_a', '$x', 'zumpus'),)
)

engine.add_rule(
    ('not', ('is_opaque', '$x')),
    (('is_a', '$x', 'tumpus'),)
)

# Add positive properties as rules
engine.add_rule(
    ('is_large', '$x'),
    (('is_a', '$x', 'vumpus'),)
)

engine.add_rule(
    ('is_feisty', '$x'),
    (('is_a', '$x', 'dumpus'),)
)

engine.add_rule(
    ('is_floral', '$x'),
    (('is_a', '$x', 'wumpus'),)
)

# Query: Is Rex not opaque? (i.e., prove is_opaque(Rex) is False)
# Since we have rules showing Rex -> rompus -> opaque, we should prove is_opaque(Rex)
# So "Rex is not opaque" would be false
result = engine.prove(('is_opaque', 'Rex'), 1)

# The answer to "Is Rex not opaque?" is the negation of whether we can prove is_opaque(Rex)
# If we can prove is_opaque(Rex), then "Rex is not opaque" is false
print("Rex is opaque:", result is not None)