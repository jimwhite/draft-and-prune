# Facts
facts.is_a("Wren", "dumpus", True)

# Rules
rule1 = rule(
    foreach=facts.is_a("?", "zumpus", True),
    then=facts.is_nervous("?", True)
)

rule2 = rule(
    foreach=facts.is_a("?", "zumpus", True),
    then=facts.is_a("?", "dumpus", True)
)

rule3 = rule(
    foreach=facts.is_a("?", "dumpus", True),
    then=facts.is_large("?", True)
)

rule4 = rule(
    foreach=facts.is_a("?", "dumpus", True),
    then=facts.is_a("?", "rompus", True)
)

rule5 = rule(
    foreach=facts.is_a("?", "rompus", True),
    then=facts.is_brown("?", True)
)

rule6 = rule(
    foreach=facts.is_a("?", "vumpus", True),
    then=facts.is_transparent("?", True)
)

rule7 = rule(
    foreach=facts.is_a("?", "rompus", True),
    then=facts.is_a("?", "numpus", True)
)

rule8 = rule(
    foreach=facts.is_a("?", "numpus", True),
    then=facts.is_bitter("?", False)
)

rule9 = rule(
    foreach=facts.is_a("?", "numpus", True),
    then=facts.is_a("?", "wumpus", True)
)

rule10 = rule(
    foreach=facts.is_a("?", "wumpus", True),
    then=facts.is_floral("?", True)
)

rule11 = rule(
    foreach=facts.is_a("?", "wumpus", True),
    then=facts.is_a("?", "yumpus", True)
)

rule12 = rule(
    foreach=facts.is_a("?", "yumpus", True),
    then=facts.is_transparent("?", False)
)

rule13 = rule(
    foreach=facts.is_a("?", "yumpus", True),
    then=facts.is_a("?", "tumpus", True)
)

rule14 = rule(
    foreach=facts.is_a("?", "tumpus", True),
    then=facts.is_bright("?", False)
)

rule15 = rule(
    foreach=facts.is_a("?", "tumpus", True),
    then=facts.is_a("?", "impus", True)
)

# Query
query = goal(facts.is_transparent("Wren", False))