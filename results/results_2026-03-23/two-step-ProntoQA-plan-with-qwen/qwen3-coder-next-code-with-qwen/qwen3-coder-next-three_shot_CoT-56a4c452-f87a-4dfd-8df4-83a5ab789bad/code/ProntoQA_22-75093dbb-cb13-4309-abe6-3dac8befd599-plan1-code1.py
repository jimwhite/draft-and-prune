# Facts
facts.is_a("Wren", "tumpus", True)

# Rules (using proper PyKe syntax)
@rule
def wumpus_is_sour(knowledge_engine, thing):
    if facts.is_a(thing, "wumpus", True):
        return facts.is_sour(thing, True)

@rule
def wumpus_is_yumpus(knowledge_engine, thing):
    if facts.is_a(thing, "wumpus", True):
        return facts.is_a(thing, "yumpus", True)

@rule
def yumpus_is_aggressive(knowledge_engine, thing):
    if facts.is_a(thing, "yumpus", True):
        return facts.is_aggressive(thing, True)

@rule
def yumpus_is_tumpus(knowledge_engine, thing):
    if facts.is_a(thing, "yumpus", True):
        return facts.is_a(thing, "tumpus", True)

@rule
def tumpus_is_transparent(knowledge_engine, thing):
    if facts.is_a(thing, "tumpus", True):
        return facts.is_transparent(thing, True)

@rule
def tumpus_is_vumpus(knowledge_engine, thing):
    if facts.is_a(thing, "tumpus", True):
        return facts.is_a(thing, "vumpus", True)

@rule
def vumpus_is_wooden(knowledge_engine, thing):
    if facts.is_a(thing, "vumpus", True):
        return facts.is_wooden(thing, True)

@rule
def vumpus_is_jompus(knowledge_engine, thing):
    if facts.is_a(thing, "vumpus", True):
        return facts.is_a(thing, "jompus", True)

@rule
def impus_is_not_feisty(knowledge_engine, thing):
    if facts.is_a(thing, "impus", True):
        return facts.is_feisty(thing, False)

@rule
def jompus_is_large(knowledge_engine, thing):
    if facts.is_a(thing, "jompus", True):
        return facts.is_large(thing, True)

@rule
def jompus_is_numpus(knowledge_engine, thing):
    if facts.is_a(thing, "jompus", True):
        return facts.is_a(thing, "numpus", True)

@rule
def numpus_is_red(knowledge_engine, thing):
    if facts.is_a(thing, "numpus", True):
        return facts.is_red(thing, True)

@rule
def numpus_is_rompus(knowledge_engine, thing):
    if facts.is_a(thing, "numpus", True):
        return facts.is_a(thing, "rompus", True)

@rule
def rompus_is_feisty(knowledge_engine, thing):
    if facts.is_a(thing, "rompus", True):
        return facts.is_feisty(thing, True)

@rule
def rompus_is_zumpus(knowledge_engine, thing):
    if facts.is_a(thing, "rompus", True):
        return facts.is_a(thing, "zumpus", True)

# Query
query = facts.is_feisty("Wren", False)