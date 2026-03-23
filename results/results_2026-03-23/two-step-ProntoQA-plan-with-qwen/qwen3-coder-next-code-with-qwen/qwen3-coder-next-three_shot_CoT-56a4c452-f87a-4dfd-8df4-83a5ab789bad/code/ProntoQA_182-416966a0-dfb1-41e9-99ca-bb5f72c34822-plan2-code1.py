from pyke import knowledge_engine

engine = knowledge_engine.engine(__file__)

# Facts
facts.is_a("Sam", "numpus", True)

# Rules
def tumpus_is_fruity():
    foreach
        facts.is_a($thing, "tumpus", True)
    assert
        facts.is_fruity($thing, True)

def tumpus_is_dumpus():
    foreach
        facts.is_a($thing, "tumpus", True)
    assert
        facts.is_a($thing, "dumpus", True)

def dumpus_is_liquid():
    foreach
        facts.is_a($thing, "dumpus", True)
    assert
        facts.is_liquid($thing, True)

def dumpus_is_numpus():
    foreach
        facts.is_a($thing, "dumpus", True)
    assert
        facts.is_a($thing, "numpus", True)

def numpus_is_sour():
    foreach
        facts.is_a($thing, "numpus", True)
    assert
        facts.is_sour($thing, True)

def numpus_is_jompus():
    foreach
        facts.is_a($thing, "numpus", True)
    assert
        facts.is_a($thing, "jompus", True)

def jompus_is_not_cold():
    foreach
        facts.is_a($thing, "jompus", True)
    assert
        facts.is_cold($thing, False)

def jompus_is_wumpus():
    foreach
        facts.is_a($thing, "jompus", True)
    assert
        facts.is_a($thing, "wumpus", True)

def wumpus_is_brown():
    foreach
        facts.is_a($thing, "wumpus", True)
    assert
        facts.is_brown($thing, True)

def wumpus_is_vumpus():
    foreach
        facts.is_a($thing, "wumpus", True)
    assert
        facts.is_a($thing, "vumpus", True)

def vumpus_is_happy():
    foreach
        facts.is_a($thing, "vumpus", True)
    assert
        facts.is_happy($thing, True)

def vumpus_is_yumpus():
    foreach
        facts.is_a($thing, "vumpus", True)
    assert
        facts.is_a($thing, "yumpus", True)

def yumpus_is_large():
    foreach
        facts.is_a($thing, "yumpus", True)
    assert
        facts.is_large($thing, True)

def yumpus_is_rompus():
    foreach
        facts.is_a($thing, "yumpus", True)
    assert
        facts.is_a($thing, "rompus", True)

def rompus_is_not_mean():
    foreach
        facts.is_a($thing, "rompus", True)
    assert
        facts.is_mean($thing, False)

def rompus_is_zumpus():
    foreach
        facts.is_a($thing, "rompus", True)
    assert
        facts.is_a($thing, "zumpus", True)

def impus_is_not_large():
    foreach
        facts.is_a($thing, "impus", True)
    assert
        facts.is_large($thing, False)

# Query
query = engine.query("facts", "is_large", ("Sam", True))