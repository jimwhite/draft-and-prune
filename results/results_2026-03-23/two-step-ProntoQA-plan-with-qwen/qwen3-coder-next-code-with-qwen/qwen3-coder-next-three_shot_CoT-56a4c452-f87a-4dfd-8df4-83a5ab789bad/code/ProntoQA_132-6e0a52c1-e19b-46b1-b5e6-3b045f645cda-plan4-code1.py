from pyke import knowledge_engine

engine = knowledge_engine.engine(__file__)

# Facts:
Facts:
is_a(Polly, vumpus, True)

# Rules:
Rules:
vumpus_is_zumpus:
    foreach is_a($thing, vumpus, True)
    assert is_a($thing, zumpus, True)

zumpus_is_dumpus:
    foreach is_a($thing, zumpus, True)
    assert is_a($thing, dumpus, True)

dumpus_is_numpus:
    foreach is_a($thing, dumpus, True)
    assert is_a($thing, numpus, True)

numpus_is_tumpus:
    foreach is_a($thing, numpus, True)
    assert is_a($thing, tumpus, True)

tumpus_is_not_blue:
    foreach is_a($thing, tumpus, True)
    assert is_blue($thing, False)

# Query:
Query:
is_blue(Polly, False)