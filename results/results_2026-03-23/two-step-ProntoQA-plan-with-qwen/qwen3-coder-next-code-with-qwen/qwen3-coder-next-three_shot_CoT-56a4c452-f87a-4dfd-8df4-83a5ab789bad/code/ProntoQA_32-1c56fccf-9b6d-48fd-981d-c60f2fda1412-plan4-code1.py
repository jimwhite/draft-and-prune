# Facts
facts.is_a("Sally", "numpus", True)

# Rules
@rule
def numpus_is_earthy(knowledge_engine):
    for thing in knowledge_engine.facts["is_a"]:
        if thing[1] == "numpus" and thing[2] is True:
            knowledge_engine.assert_fact(("is_earthy", thing[0], True))

@rule
def numpus_is_vumpus(knowledge_engine):
    for thing in knowledge_engine.facts["is_a"]:
        if thing[1] == "numpus" and thing[2] is True:
            knowledge_engine.assert_fact(("is_a", thing[0], "vumpus"))

@rule
def vumpus_is_transparent(knowledge_engine):
    for thing in knowledge_engine.facts["is_a"]:
        if thing[1] == "vumpus" and thing[2] is True:
            knowledge_engine.assert_fact(("is_transparent", thing[0], True))

@rule
def vumpus_is_tumpus(knowledge_engine):
    for thing in knowledge_engine.facts["is_a"]:
        if thing[1] == "vumpus" and thing[2] is True:
            knowledge_engine.assert_fact(("is_a", thing[0], "tumpus"))

@rule
def tumpus_is_small(knowledge_engine):
    for thing in knowledge_engine.facts["is_a"]:
        if thing[1] == "tumpus" and thing[2] is True:
            knowledge_engine.assert_fact(("is_small", thing[0], True))

@rule
def tumpus_is_dumpus(knowledge_engine):
    for thing in knowledge_engine.facts["is_a"]:
        if thing[1] == "tumpus" and thing[2] is True:
            knowledge_engine.assert_fact(("is_a", thing[0], "dumpus"))

@rule
def dumpus_is_not_aggressive(knowledge_engine):
    for thing in knowledge_engine.facts["is_a"]:
        if thing[1] == "dumpus" and thing[2] is True:
            knowledge_engine.assert_fact(("is_aggressive", thing[0], False))

@rule
def dumpus_is_wumpus(knowledge_engine):
    for thing in knowledge_engine.facts["is_a"]:
        if thing[1] == "dumpus" and thing[2] is True:
            knowledge_engine.assert_fact(("is_a", thing[0], "wumpus"))

@rule
def wumpus_is_not_wooden(knowledge_engine):
    for thing in knowledge_engine.facts["is_a"]:
        if thing[1] == "wumpus" and thing[2] is True:
            knowledge_engine.assert_fact(("is_wooden", thing[0], False))

@rule
def wumpus_is_jompus(knowledge_engine):
    for thing in knowledge_engine.facts["is_a"]:
        if thing[1] == "wumpus" and thing[2] is True:
            knowledge_engine.assert_fact(("is_a", thing[0], "jompus"))

@rule
def jompus_is_not_nervous(knowledge_engine):
    for thing in knowledge_engine.facts["is_a"]:
        if thing[1] == "jompus" and thing[2] is True:
            knowledge_engine.assert_fact(("is_nervous", thing[0], False))

@rule
def jompus_is_zumpus(knowledge_engine):
    for thing in knowledge_engine.facts["is_a"]:
        if thing[1] == "jompus" and thing[2] is True:
            knowledge_engine.assert_fact(("is_a", thing[0], "zumpus"))

@rule
def zumpus_is_temperate(knowledge_engine):
    for thing in knowledge_engine.facts["is_a"]:
        if thing[1] == "zumpus" and thing[2] is True:
            knowledge_engine.assert_fact(("is_temperate", thing[0], True))

@rule
def rompus_is_wooden(knowledge_engine):
    for thing in knowledge_engine.facts["is_a"]:
        if thing[1] == "rompus" and thing[2] is True:
            knowledge_engine.assert_fact(("is_wooden", thing[0], True))

@rule
def zumpus_is_impus(knowledge_engine):
    for thing in knowledge_engine.facts["is_a"]:
        if thing[1] == "zumpus" and thing[2] is True:
            knowledge_engine.assert_fact(("is_a", thing[0], "impus"))

@rule
def impus_is_blue(knowledge_engine):
    for thing in knowledge_engine.facts["is_a"]:
        if thing[1] == "impus" and thing[2] is True:
            knowledge_engine.assert_fact(("is_blue", thing[0], True))

@rule
def impus_is_yumpus(knowledge_engine):
    for thing in knowledge_engine.facts["is_a"]:
        if thing[1] == "impus" and thing[2] is True:
            knowledge_engine.assert_fact(("is_a", thing[0], "yumpus"))

# Query
query = facts.is_wooden("Sally", False)