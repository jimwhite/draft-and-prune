# Facts
facts.is_a("Polly", "vumpus", True)

# Rules
k.rule(
    foreach=facts.is_a("?", "vumpus", True),
    then=facts.is_transparent("$0", True)
)

k.rule(
    foreach=facts.is_a("?", "vumpus", True),
    then=facts.is_a("$0", "zumpus", True)
)

k.rule(
    foreach=facts.is_a("?", "zumpus", True),
    then=facts.is_large("$0", False)
)

k.rule(
    foreach=facts.is_a("?", "zumpus", True),
    then=facts.is_a("$0", "dumpus", True)
)

k.rule(
    foreach=facts.is_a("?", "dumpus", True),
    then=facts.is_spicy("$0", True)
)

k.rule(
    foreach=facts.is_a("?", "dumpus", True),
    then=facts.is_a("$0", "numpus", True)
)

k.rule(
    foreach=facts.is_a("?", "impus", True),
    then=facts.is_blue("$0", True)
)

k.rule(
    foreach=facts.is_a("?", "numpus", True),
    then=facts.is_temperate("$0", True)
)

k.rule(
    foreach=facts.is_a("?", "numpus", True),
    then=facts.is_a("$0", "tumpus", True)
)

k.rule(
    foreach=facts.is_a("?", "tumpus", True),
    then=facts.is_blue("$0", False)
)

k.rule(
    foreach=facts.is_a("?", "tumpus", True),
    then=facts.is_a("$0", "jompus", True)
)

k.rule(
    foreach=facts.is_a("?", "jompus", True),
    then=facts.is_happy("$0", True)
)

k.rule(
    foreach=facts.is_a("?", "jompus", True),
    then=facts.is_a("$0", "yumpus", True)
)

k.rule(
    foreach=facts.is_a("?", "yumpus", True),
    then=facts.is_amenable("$0", False)
)

k.rule(
    foreach=facts.is_a("?", "yumpus", True),
    then=facts.is_a("$0", "wumpus", True)
)

k.rule(
    foreach=facts.is_a("?", "wumpus", True),
    then=facts.is_floral("$0", False)
)

k.rule(
    foreach=facts.is_a("?", "wumpus", True),
    then=facts.is_a("$0", "rompus", True)
)

# Query
k.query(facts.is_blue("Polly", False))