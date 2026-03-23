# Facts
facts.is_a("Stella", "numpus", True)

# Rules
@rule
def zumpus_is_metallic():
    foreach(
        facts.is_a(thing, "zumpus", True)
    )
    assert(
        facts.is_metallic(thing, True)
    )

@rule
def zumpus_is_wumpus():
    foreach(
        facts.is_a(thing, "zumpus", True)
    )
    assert(
        facts.is_a(thing, "wumpus", True)
    )

@rule
def wumpus_is_not_floral():
    foreach(
        facts.is_a(thing, "wumpus", True)
    )
    assert(
        facts.is_floral(thing, False)
    )

@rule
def wumpus_is_numpus():
    foreach(
        facts.is_a(thing, "wumpus", True)
    )
    assert(
        facts.is_a(thing, "numpus", True)
    )

@rule
def numpus_is_happy():
    foreach(
        facts.is_a(thing, "numpus", True)
    )
    assert(
        facts.is_happy(thing, True)
    )

@rule
def numpus_is_impus():
    foreach(
        facts.is_a(thing, "numpus", True)
    )
    assert(
        facts.is_a(thing, "impus", True)
    )

@rule
def impus_is_kind():
    foreach(
        facts.is_a(thing, "impus", True)
    )
    assert(
        facts.is_kind(thing, True)
    )

@rule
def impus_is_rompus():
    foreach(
        facts.is_a(thing, "impus", True)
    )
    assert(
        facts.is_a(thing, "rompus", True)
    )

@rule
def rompus_is_large():
    foreach(
        facts.is_a(thing, "rompus", True)
    )
    assert(
        facts.is_large(thing, True)
    )

@rule
def vumpus_is_opaque():
    foreach(
        facts.is_a(thing, "vumpus", True)
    )
    assert(
        facts.is_opaque(thing, True)
    )

@rule
def rompus_is_jompus():
    foreach(
        facts.is_a(thing, "rompus", True)
    )
    assert(
        facts.is_a(thing, "jompus", True)
    )

@rule
def jompus_is_cold():
    foreach(
        facts.is_a(thing, "jompus", True)
    )
    assert(
        facts.is_cold(thing, True)
    )

@rule
def jompus_is_dumpus():
    foreach(
        facts.is_a(thing, "jompus", True)
    )
    assert(
        facts.is_a(thing, "dumpus", True)
    )

@rule
def dumpus_is_not_opaque():
    foreach(
        facts.is_a(thing, "dumpus", True)
    )
    assert(
        facts.is_opaque(thing, False)
    )

@rule
def dumpus_is_yumpus():
    foreach(
        facts.is_a(thing, "dumpus", True)
    )
    assert(
        facts.is_a(thing, "yumpus", True)
    )

@rule
def yumpus_is_spicy():
    foreach(
        facts.is_a(thing, "yumpus", True)
    )
    assert(
        facts.is_spicy(thing, True)
    )

@rule
def yumpus_is_tumpus():
    foreach(
        facts.is_a(thing, "yumpus", True)
    )
    assert(
        facts.is_a(thing, "tumpus", True)
    )

# Query
query_result = facts.is_opaque("Stella", True)