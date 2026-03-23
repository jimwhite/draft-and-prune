from pyke import knowledge_engine

engine = knowledge_engine.engine(__file__)

# Facts
engine.add_predicate("is_a", "Rex", "zumpus", True)

# Rules
@engine.rule("zumpus_is_not_temperate")
def zumpus_is_not_temperate():
    return [
        (lambda thing: ("is_a", thing, "zumpus", True), 
         lambda thing: [("is_temperate", thing, False)])
    ]

@engine.rule("zumpus_is_vumpus")
def zumpus_is_vumpus():
    return [
        (lambda thing: ("is_a", thing, "zumpus", True), 
         lambda thing: [("is_a", thing, "vumpus", True)])
    ]

@engine.rule("vumpus_is_large")
def vumpus_is_large():
    return [
        (lambda thing: ("is_a", thing, "vumpus", True), 
         lambda thing: [("is_large", thing, True)])
    ]

@engine.rule("vumpus_is_dumpus")
def vumpus_is_dumpus():
    return [
        (lambda thing: ("is_a", thing, "vumpus", True), 
         lambda thing: [("is_a", thing, "dumpus", True)])
    ]

@engine.rule("dumpus_is_feisty")
def dumpus_is_feisty():
    return [
        (lambda thing: ("is_a", thing, "dumpus", True), 
         lambda thing: [("is_feisty", thing, True)])
    ]

@engine.rule("tumpus_is_not_opaque")
def tumpus_is_not_opaque():
    return [
        (lambda thing: ("is_a", thing, "tumpus", True), 
         lambda thing: [("is_opaque", thing, False)])
    ]

@engine.rule("dumpus_is_wumpus")
def dumpus_is_wumpus():
    return [
        (lambda thing: ("is_a", thing, "dumpus", True), 
         lambda thing: [("is_a", thing, "wumpus", True)])
    ]

@engine.rule("wumpus_is_floral")
def wumpus_is_floral():
    return [
        (lambda thing: ("is_a", thing, "wumpus", True), 
         lambda thing: [("is_floral", thing, True)])
    ]

@engine.rule("wumpus_is_rompus")
def wumpus_is_rompus():
    return [
        (lambda thing: ("is_a", thing, "wumpus", True), 
         lambda thing: [("is_a", thing, "rompus", True)])
    ]

@engine.rule("rompus_is_opaque")
def rompus_is_opaque():
    return [
        (lambda thing: ("is_a", thing, "rompus", True), 
         lambda thing: [("is_opaque", thing, True)])
    ]

@engine.rule("rompus_is_numpus")
def rompus_is_numpus():
    return [
        (lambda thing: ("is_a", thing, "rompus", True), 
         lambda thing: [("is_a", thing, "numpus", True)])
    ]

# Activate the rules
engine.activate("rules")

# Query: Is Rex not opaque?
result = engine.query("is_opaque", "Rex", False)

# Since we want to check if "Rex is not opaque" is true, 
# and the query checks if is_opaque(Rex) = False,
# we need to negate the result
is_rex_not_opaque = not result

print(f"Rex is opaque: {result}")
print(f"Statement 'Rex is not opaque' is: {is_rex_not_opaque}")