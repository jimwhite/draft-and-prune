from pyke import knowledge_engine, facts

# Facts
facts.is_a("Wren", "yumpus", True)

# Rules
@rule(
    foreach=facts.is_a("$thing", "jompus", True),
    then=facts.is_bright("$thing", True)
)
def jompus_is_bright():
    pass

@rule(
    foreach=facts.is_a("$thing", "jompus", True),
    then=facts.is_a("$thing", "vumpus", True)
)
def jompus_is_vumpus():
    pass

@rule(
    foreach=facts.is_a("$thing", "vumpus", True),
    then=facts.is_floral("$thing", True)
)
def vumpus_is_floral():
    pass

@rule(
    foreach=facts.is_a("$thing", "vumpus", True),
    then=facts.is_a("$thing", "yumpus", True)
)
def vumpus_is_yumpus():
    pass

@rule(
    foreach=facts.is_a("$thing", "yumpus", True),
    then=facts.is_temperate("$thing", False)
)
def yumpus_is_not_temperate():
    pass

@rule(
    foreach=facts.is_a("$thing", "yumpus", True),
    then=facts.is_a("$thing", "numpus", True)
)
def yumpus_is_numpus():
    pass

@rule(
    foreach=facts.is_a("$thing", "numpus", True),
    then=facts.is_sweet("$thing", True)
)
def numpus_is_sweet():
    pass

@rule(
    foreach=facts.is_a("$thing", "numpus", True),
    then=facts.is_a("$thing", "zumpus", True)
)
def numpus_is_zumpus():
    pass

@rule(
    foreach=facts.is_a("$thing", "zumpus", True),
    then=facts.is_mean("$thing", True)
)
def zumpus_is_mean():
    pass

@rule(
    foreach=facts.is_a("$thing", "zumpus", True),
    then=facts.is_a("$thing", "rompus", True)
)
def zumpus_is_rompus():
    pass

@rule(
    foreach=facts.is_a("$thing", "rompus", True),
    then=facts.is_feisty("$thing", False)
)
def rompus_is_not_feisty():
    pass

@rule(
    foreach=facts.is_a("$thing", "impus", True),
    then=facts.is_transparent("$thing", False)
)
def impus_is_not_transparent():
    pass

@rule(
    foreach=facts.is_a("$thing", "rompus", True),
    then=facts.is_a("$thing", "wumpus", True)
)
def rompus_is_wumpus():
    pass

@rule(
    foreach=facts.is_a("$thing", "wumpus", True),
    then=facts.is_transparent("$thing", True)
)
def wumpus_is_transparent():
    pass

@rule(
    foreach=facts.is_a("$thing", "wumpus", True),
    then=facts.is_a("$thing", "dumpus", True)
)
def wumpus_is_dumpus():
    pass

@rule(
    foreach=facts.is_a("$thing", "dumpus", True),
    then=facts.is_large("$thing", True)
)
def dumpus_is_large():
    pass

@rule(
    foreach=facts.is_a("$thing", "dumpus", True),
    then=facts.is_a("$thing", "tumpus", True)
)
def dumpus_is_tumpus():
    pass

# Query
query_result = facts.is_transparent("Wren", True)