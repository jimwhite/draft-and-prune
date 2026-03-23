# Facts
facts.is_a("Fae", "dumpus")

# Rules
rule.dumpus_to_zumpus:
    foreach is_a(?x, "dumpus")
    assert is_a(?x, "zumpus")

rule.zumpus_to_yumpus:
    foreach is_a(?x, "zumpus")
    assert is_a(?x, "yumpus")

rule.yumpus_to_rompus:
    foreach is_a(?x, "yumpus")
    assert is_a(?x, "rompus")

rule.rompus_to_impus:
    foreach is_a(?x, "rompus")
    assert is_a(?x, "impus")

rule.impus_not_floral:
    foreach is_a(?x, "impus")
    assert not is_floral(?x)

# Query
query.is_fae_not_floral:
    goal not is_floral("Fae")