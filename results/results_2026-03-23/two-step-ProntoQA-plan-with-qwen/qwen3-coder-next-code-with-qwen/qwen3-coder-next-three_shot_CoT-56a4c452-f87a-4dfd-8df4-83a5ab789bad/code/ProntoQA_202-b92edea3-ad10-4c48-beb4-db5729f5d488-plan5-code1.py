# Facts
facts.is_a("Wren", "zumpus", True)

# Rules
@rule
def tumpus_is_temperate(knowledge_engine):
    for thing in knowledge_engine.facts["is_a"]:
        if thing[1] == "tumpus" and thing[2] is True:
            knowledge_engine.assert_fact(("is_temperate", thing[0], True))

@rule
def tumpus_is_impus(knowledge_engine):
    for thing in knowledge_engine.facts["is_a"]:
        if thing[1] == "tumpus" and thing[2] is True:
            knowledge_engine.assert_fact(("is_a", thing[0], "impus", True))

@rule
def impus_is_orange(knowledge_engine):
    for thing in knowledge_engine.facts["is_a"]:
        if thing[1] == "impus" and thing[2] is True:
            knowledge_engine.assert_fact(("is_orange", thing[0], True))

@rule
def impus_is_yumpus(knowledge_engine):
    for thing in knowledge_engine.facts["is_a"]:
        if thing[1] == "impus" and thing[2] is True:
            knowledge_engine.assert_fact(("is_a", thing[0], "yumpus", True))

@rule
def yumpus_is_shy(knowledge_engine):
    for thing in knowledge_engine.facts["is_a"]:
        if thing[1] == "yumpus" and thing[2] is True:
            knowledge_engine.assert_fact(("is_shy", thing[0], True))

@rule
def yumpus_is_zumpus(knowledge_engine):
    for thing in knowledge_engine.facts["is_a"]:
        if thing[1] == "yumpus" and thing[2] is True:
            knowledge_engine.assert_fact(("is_a", thing[0], "zumpus", True))

@rule
def zumpus_is_bright(knowledge_engine):
    for thing in knowledge_engine.facts["is_a"]:
        if thing[1] == "zumpus" and thing[2] is True:
            knowledge_engine.assert_fact(("is_bright", thing[0], True))

@rule
def zumpus_is_rompus(knowledge_engine):
    for thing in knowledge_engine.facts["is_a"]:
        if thing[1] == "zumpus" and thing[2] is True:
            knowledge_engine.assert_fact(("is_a", thing[0], "rompus", True))

@rule
def numpus_is_opaque(knowledge_engine):
    for thing in knowledge_engine.facts["is_a"]:
        if thing[1] == "numpus" and thing[2] is True:
            knowledge_engine.assert_fact(("is_opaque", thing[0], True))

@rule
def rompus_is_small(knowledge_engine):
    for thing in knowledge_engine.facts["is_a"]:
        if thing[1] == "rompus" and thing[2] is True:
            knowledge_engine.assert_fact(("is_small", thing[0], True))

@rule
def rompus_is_dumpus(knowledge_engine):
    for thing in knowledge_engine.facts["is_a"]:
        if thing[1] == "rompus" and thing[2] is True:
            knowledge_engine.assert_fact(("is_a", thing[0], "dumpus", True))

@rule
def dumpus_is_not_floral(knowledge_engine):
    for thing in knowledge_engine.facts["is_a"]:
        if thing[1] == "dumpus" and thing[2] is True:
            knowledge_engine.assert_fact(("is_floral", thing[0], False))

@rule
def dumpus_is_wumpus(knowledge_engine):
    for thing in knowledge_engine.facts["is_a"]:
        if thing[1] == "dumpus" and thing[2] is True:
            knowledge_engine.assert_fact(("is_a", thing[0], "wumpus", True))

@rule
def wumpus_is_aggressive(knowledge_engine):
    for thing in knowledge_engine.facts["is_a"]:
        if thing[1] == "wumpus" and thing[2] is True:
            knowledge_engine.assert_fact(("is_aggressive", thing[0], True))

@rule
def wumpus_is_vumpus(knowledge_engine):
    for thing in knowledge_engine.facts["is_a"]:
        if thing[1] == "wumpus" and thing[2] is True:
            knowledge_engine.assert_fact(("is_a", thing[0], "vumpus", True))

@rule
def vumpus_is_not_opaque(knowledge_engine):
    for thing in knowledge_engine.facts["is_a"]:
        if thing[1] == "vumpus" and thing[2] is True:
            knowledge_engine.assert_fact(("is_opaque", thing[0], False))

@rule
def vumpus_is_jompus(knowledge_engine):
    for thing in knowledge_engine.facts["is_a"]:
        if thing[1] == "vumpus" and thing[2] is True:
            knowledge_engine.assert_fact(("is_a", thing[0], "jompus", True))

# Query
query = facts.is_opaque("Wren", True)