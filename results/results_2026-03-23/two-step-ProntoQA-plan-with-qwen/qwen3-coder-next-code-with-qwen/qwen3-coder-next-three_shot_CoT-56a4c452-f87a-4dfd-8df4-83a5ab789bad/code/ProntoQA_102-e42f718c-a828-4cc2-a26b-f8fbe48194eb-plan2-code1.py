from pyke import knowledge_engine

# Create knowledge engine instance
engine = knowledge_engine.engine(__file__)

# Facts
facts.is_a("Rex", "wumpus", True)

# Rules
dumpus_is_not_dull:
    foreach
        facts.is_a($thing, "dumpus", True)
    assert
        facts.is_dull($thing, False)

tumpus_is_not_spicy:
    foreach
        facts.is_a($thing, "tumpus", True)
    assert
        facts.is_spicy($thing, False)

dumpus_is_vumpus:
    foreach
        facts.is_a($thing, "dumpus", True)
    assert
        facts.is_a($thing, "vumpus", True)

vumpus_is_fruity:
    foreach
        facts.is_a($thing, "vumpus", True)
    assert
        facts.is_fruity($thing, True)

vumpus_is_zumpus:
    foreach
        facts.is_a($thing, "vumpus", True)
    assert
        facts.is_a($thing, "zumpus", True)

zumpus_is_large:
    foreach
        facts.is_a($thing, "zumpus", True)
    assert
        facts.is_large($thing, True)

zumpus_is_wumpus:
    foreach
        facts.is_a($thing, "zumpus", True)
    assert
        facts.is_a($thing, "wumpus", True)

wumpus_is_blue:
    foreach
        facts.is_a($thing, "wumpus", True)
    assert
        facts.is_blue($thing, True)

wumpus_is_numpus:
    foreach
        facts.is_a($thing, "wumpus", True)
    assert
        facts.is_a($thing, "numpus", True)

numpus_is_kind:
    foreach
        facts.is_a($thing, "numpus", True)
    assert
        facts.is_kind($thing, True)

numpus_is_rompus:
    foreach
        facts.is_a($thing, "numpus", True)
    assert
        facts.is_a($thing, "rompus", True)

rompus_is_cold:
    foreach
        facts.is_a($thing, "rompus", True)
    assert
        facts.is_cold($thing, True)

rompus_is_jompus:
    foreach
        facts.is_a($thing, "rompus", True)
    assert
        facts.is_a($thing, "jompus", True)

jompus_is_not_transparent:
    foreach
        facts.is_a($thing, "jompus", True)
    assert
        facts.is_transparent($thing, False)

jompus_is_yumpus:
    foreach
        facts.is_a($thing, "jompus", True)
    assert
        facts.is_a($thing, "yumpus", True)

yumpus_is_spicy:
    foreach
        facts.is_a($thing, "yumpus", True)
    assert
        facts.is_spicy($thing, True)

yumpus_is_impus:
    foreach
        facts.is_a($thing, "yumpus", True)
    assert
        facts.is_a($thing, "impus", True)

# Query - check if Rex is not spicy (i.e., is_spicy("Rex", False))
# Since we know Rex is a wumpus, and through the chain of inclusions,
# Rex becomes a yumpus, which is spicy, so this query should fail
facts.is_spicy("Rex", False)