from pyke import knowledge_engine, facts, rules

# Create knowledge engine instance
engine = knowledge_engine.engine(__name__)

# Facts
engine.facts.add(("is_a", "Fae", "numpus", True))

# Rules
@rules.rule(
    foreach=[
        facts.is_a("$thing", "rompus", True)
    ],
    then=[
        facts.is_metallic("$thing", True)
    ]
)
def rompus_is_metallic():
    pass

@rules.rule(
    foreach=[
        facts.is_a("$thing", "rompus", True)
    ],
    then=[
        facts.is_a("$thing", "dumpus", True)
    ]
)
def rompus_is_dumpus():
    pass

@rules.rule(
    foreach=[
        facts.is_a("$thing", "dumpus", True)
    ],
    then=[
        facts.is_blue("$thing", True)
    ]
)
def dumpus_is_blue():
    pass

@rules.rule(
    foreach=[
        facts.is_a("$thing", "dumpus", True)
    ],
    then=[
        facts.is_a("$thing", "numpus", True)
    ]
)
def dumpus_is_numpus():
    pass

@rules.rule(
    foreach=[
        facts.is_a("$thing", "numpus", True)
    ],
    then=[
        facts.is_fruity("$thing", True)
    ]
)
def numpus_is_fruity():
    pass

@rules.rule(
    foreach=[
        facts.is_a("$thing", "numpus", True)
    ],
    then=[
        facts.is_a("$thing", "jompus", True)
    ]
)
def numpus_is_jompus():
    pass

@rules.rule(
    foreach=[
        facts.is_a("$thing", "jompus", True)
    ],
    then=[
        facts.is_mean("$thing", True)
    ]
)
def jompus_is_mean():
    pass

@rules.rule(
    foreach=[
        facts.is_a("$thing", "jompus", True)
    ],
    then=[
        facts.is_a("$thing", "tumpus", True)
    ]
)
def jompus_is_tumpus():
    pass

@rules.rule(
    foreach=[
        facts.is_a("$thing", "tumpus", True)
    ],
    then=[
        facts.is_temperate("$thing", False)
    ]
)
def tumpus_is_not_temperate():
    pass

@rules.rule(
    foreach=[
        facts.is_a("$thing", "tumpus", True)
    ],
    then=[
        facts.is_a("$thing", "impus", True)
    ]
)
def tumpus_is_impus():
    pass

@rules.rule(
    foreach=[
        facts.is_a("$thing", "impus", True)
    ],
    then=[
        facts.is_dull("$thing", False)
    ]
)
def impus_is_not_dull():
    pass

@rules.rule(
    foreach=[
        facts.is_a("$thing", "impus", True)
    ],
    then=[
        facts.is_a("$thing", "yumpus", True)
    ]
)
def impus_is_yumpus():
    pass

@rules.rule(
    foreach=[
        facts.is_a("$thing", "yumpus", True)
    ],
    then=[
        facts.is_transparent("$thing", False)
    ]
)
def yumpus_is_not_transparent():
    pass

@rules.rule(
    foreach=[
        facts.is_a("$thing", "yumpus", True)
    ],
    then=[
        facts.is_a("$thing", "zumpus", True)
    ]
)
def yumpus_is_zumpus():
    pass

@rules.rule(
    foreach=[
        facts.is_a("$thing", "wumpus", True)
    ],
    then=[
        facts.is_transparent("$thing", True)
    ]
)
def wumpus_is_transparent():
    pass

@rules.rule(
    foreach=[
        facts.is_a("$thing", "zumpus", True)
    ],
    then=[
        facts.is_sweet("$thing", False)
    ]
)
def zumpus_is_not_sweet():
    pass

@rules.rule(
    foreach=[
        facts.is_a("$thing", "zumpus", True)
    ],
    then=[
        facts.is_a("$thing", "vumpus", True)
    ]
)
def zumpus_is_vumpus():
    pass

# Activate the knowledge base
engine.activate("rules")

# Query: Is Fae transparent?
result = engine.facts.is_transparent("Fae", True)