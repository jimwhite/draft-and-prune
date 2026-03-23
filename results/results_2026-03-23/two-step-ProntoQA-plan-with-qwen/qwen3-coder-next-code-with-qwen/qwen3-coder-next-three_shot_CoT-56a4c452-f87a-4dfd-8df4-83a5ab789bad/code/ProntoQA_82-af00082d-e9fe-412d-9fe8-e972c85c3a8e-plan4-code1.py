from pyke import knowledge_engine

kb = knowledge_engine.engine(__file__)

# Facts
facts = kb.add_facts('facts')
facts.is_a("Rex", "yumpus", True)

# Rules
rules = kb.add_rules('rules')

# Rule: Each impus is a yumpus.
@kb.rule
def impus_is_yumpus():
    return (
        (facts.is_a, '$thing', 'impus', True),
        facts.assert_(('is_a', '$thing', 'yumpus', True))
    )

# Rule: Yumpuses are blue.
@kb.rule
def yumpus_is_blue():
    return (
        (facts.is_a, '$thing', 'yumpus', True),
        facts.assert_(('is_blue', '$thing', True))
    )

# Rule: Yumpuses are wumpuses.
@kb.rule
def yumpus_is_wumpus():
    return (
        (facts.is_a, '$thing', 'yumpus', True),
        facts.assert_(('is_a', '$thing', 'wumpus', True))
    )

# Rule: Wumpuses are hot.
@kb.rule
def wumpus_is_hot():
    return (
        (facts.is_a, '$thing', 'wumpus', True),
        facts.assert_(('is_hot', '$thing', True))
    )

# Rule: Every wumpus is a numpus.
@kb.rule
def wumpus_is_numpus():
    return (
        (facts.is_a, '$thing', 'wumpus', True),
        facts.assert_(('is_a', '$thing', 'numpus', True))
    )

# Rule: Jompuses are happy.
@kb.rule
def jompus_is_happy():
    return (
        (facts.is_a, '$thing', 'jompus', True),
        facts.assert_(('is_happy', '$thing', True))
    )

# Rule: Numpuses are fruity.
@kb.rule
def numpus_is_fruity():
    return (
        (facts.is_a, '$thing', 'numpus', True),
        facts.assert_(('is_fruity', '$thing', True))
    )

# Rule: Numpuses are dumpuses.
@kb.rule
def numpus_is_dumpus():
    return (
        (facts.is_a, '$thing', 'numpus', True),
        facts.assert_(('is_a', '$thing', 'dumpus', True))
    )

# Rule: Every dumpus is not dull.
@kb.rule
def dumpus_is_not_dull():
    return (
        (facts.is_a, '$thing', 'dumpus', True),
        facts.assert_(('is_dull', '$thing', False))
    )

# Rule: Every dumpus is a tumpus.
@kb.rule
def dumpus_is_tumpus():
    return (
        (facts.is_a, '$thing', 'dumpus', True),
        facts.assert_(('is_a', '$thing', 'tumpus', True))
    )

# Rule: Tumpuses are not happy.
@kb.rule
def tumpus_is_not_happy():
    return (
        (facts.is_a, '$thing', 'tumpus', True),
        facts.assert_(('is_happy', '$thing', False))
    )

# Rule: Every tumpus is a vumpus.
@kb.rule
def tumpus_is_vumpus():
    return (
        (facts.is_a, '$thing', 'tumpus', True),
        facts.assert_(('is_a', '$thing', 'vumpus', True))
    )

# Rule: Vumpuses are not opaque.
@kb.rule
def vumpus_is_not_opaque():
    return (
        (facts.is_a, '$thing', 'vumpus', True),
        facts.assert_(('is_opaque', '$thing', False))
    )

# Rule: Every vumpus is a rompus.
@kb.rule
def vumpus_is_rompus():
    return (
        (facts.is_a, '$thing', 'vumpus', True),
        facts.assert_(('is_a', '$thing', 'rompus', True))
    )

# Rule: Rompuses are metallic.
@kb.rule
def rompus_is_metallic():
    return (
        (facts.is_a, '$thing', 'rompus', True),
        facts.assert_(('is_metallic', '$thing', True))
    )

# Rule: Each rompus is a zumpus.
@kb.rule
def rompus_is_zumpus():
    return (
        (facts.is_a, '$thing', 'rompus', True),
        facts.assert_(('is_a', '$thing', 'zumpus', True))
    )

# Query
query = kb.add_query('query')

@kb.query
def check_rex_happiness():
    return facts.is_a("Rex", "yumpus", True) & ~facts.is_happy("Rex", True)