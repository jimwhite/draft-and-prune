from pyke import knowledge_engine

engine = knowledge_engine.engine(__file__)

# Facts
engine.add_predicate("is_a", "Rex", "zumpus", True)

# Rules
@engine.rule("zumpus_is_not_temperate")
def zumpus_is_not_temperate():
    engine.add_predicate("is_temperate", "$thing", False)
    return [("is_a", "$thing", "zumpus", True)]

@engine.rule("zumpus_is_vumpus")
def zumpus_is_vumpus():
    engine.add_predicate("is_a", "$thing", "vumpus", True)
    return [("is_a", "$thing", "zumpus", True)]

@engine.rule("vumpus_is_large")
def vumpus_is_large():
    engine.add_predicate("is_large", "$thing", True)
    return [("is_a", "$thing", "vumpus", True)]

@engine.rule("vumpus_is_dumpus")
def vumpus_is_dumpus():
    engine.add_predicate("is_a", "$thing", "dumpus", True)
    return [("is_a", "$thing", "vumpus", True)]

@engine.rule("dumpus_is_feisty")
def dumpus_is_feisty():
    engine.add_predicate("is_feisty", "$thing", True)
    return [("is_a", "$thing", "dumpus", True)]

@engine.rule("tumpus_is_not_opaque")
def tumpus_is_not_opaque():
    engine.add_predicate("is_opaque", "$thing", False)
    return [("is_a", "$thing", "tumpus", True)]

@engine.rule("dumpus_is_wumpus")
def dumpus_is_wumpus():
    engine.add_predicate("is_a", "$thing", "wumpus", True)
    return [("is_a", "$thing", "dumpus", True)]

@engine.rule("wumpus_is_floral")
def wumpus_is_floral():
    engine.add_predicate("is_floral", "$thing", True)
    return [("is_a", "$thing", "wumpus", True)]

@engine.rule("wumpus_is_rompus")
def wumpus_is_rompus():
    engine.add_predicate("is_a", "$thing", "rompus", True)
    return [("is_a", "$thing", "wumpus", True)]

@engine.rule("rompus_is_opaque")
def rompus_is_opaque():
    engine.add_predicate("is_opaque", "$thing", True)
    return [("is_a", "$thing", "rompus", True)]

@engine.rule("rompus_is_numpus")
def rompus_is_numpus():
    engine.add_predicate("is_a", "$thing", "numpus", True)
    return [("is_a", "$thing", "rompus", True)]

# Query
result = engine.query("is_opaque", "Rex", False)
print(not result)  # Returns True if "Rex is not opaque" is true, False otherwise