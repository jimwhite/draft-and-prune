from pyke import knowledge_engine

# Create knowledge engine instance
engine = knowledge_engine.engine(__file__)

# Facts
facts.is_a("Stella", "yumpus", True)

# Rules
@rule(
    foreach=[
        facts.is_a($thing, "tumpus", True),
    ],
    then=[
        facts.is_angry($thing, False)
    ]
)
def tumpus_is_not_angry(context, $thing):
    pass

@rule(
    foreach=[
        facts.is_a($thing, "tumpus", True),
    ],
    then=[
        facts.is_a($thing, "rompus", True)
    ]
)
def tumpus_is_rompus(context, $thing):
    pass

@rule(
    foreach=[
        facts.is_a($thing, "numpus", True),
    ],
    then=[
        facts.is_bright($thing, False)
    ]
)
def numpus_is_not_bright(context, $thing):
    pass

@rule(
    foreach=[
        facts.is_a($thing, "rompus", True),
    ],
    then=[
        facts.is_luminous($thing, False)
    ]
)
def rompus_is_not_luminous(context, $thing):
    pass

@rule(
    foreach=[
        facts.is_a($thing, "rompus", True),
    ],
    then=[
        facts.is_a($thing, "yumpus", True)
    ]
)
def rompus_is_yumpus(context, $thing):
    pass

@rule(
    foreach=[
        facts.is_a($thing, "yumpus", True),
    ],
    then=[
        facts.is_transparent($thing, True)
    ]
)
def yumpus_is_transparent(context, $thing):
    pass

@rule(
    foreach=[
        facts.is_a($thing, "yumpus", True),
    ],
    then=[
        facts.is_a($thing, "zumpus", True)
    ]
)
def yumpus_is_zumpus(context, $thing):
    pass

@rule(
    foreach=[
        facts.is_a($thing, "zumpus", True),
    ],
    then=[
        facts.is_bitter($thing, False)
    ]
)
def zumpus_is_not_bitter(context, $thing):
    pass

@rule(
    foreach=[
        facts.is_a($thing, "zumpus", True),
    ],
    then=[
        facts.is_a($thing, "impus", True)
    ]
)
def zumpus_is_impus(context, $thing):
    pass

@rule(
    foreach=[
        facts.is_a($thing, "impus", True),
    ],
    then=[
        facts.is_red($thing, True)
    ]
)
def impus_is_red(context, $thing):
    pass

@rule(
    foreach=[
        facts.is_a($thing, "impus", True),
    ],
    then=[
        facts.is_a($thing, "dumpus", True)
    ]
)
def impus_is_dumpus(context, $thing):
    pass

@rule(
    foreach=[
        facts.is_a($thing, "dumpus", True),
    ],
    then=[
        facts.is_happy($thing, True)
    ]
)
def dumpus_is_happy(context, $thing):
    pass

@rule(
    foreach=[
        facts.is_a($thing, "dumpus", True),
    ],
    then=[
        facts.is_a($thing, "vumpus", True)
    ]
)
def dumpus_is_vumpus(context, $thing):
    pass

@rule(
    foreach=[
        facts.is_a($thing, "vumpus", True),
    ],
    then=[
        facts.is_bright($thing, True)
    ]
)
def vumpus_is_bright(context, $thing):
    pass

@rule(
    foreach=[
        facts.is_a($thing, "vumpus", True),
    ],
    then=[
        facts.is_a($thing, "jompus", True)
    ]
)
def vumpus_is_jompus(context, $thing):
    pass

@rule(
    foreach=[
        facts.is_a($thing, "jompus", True),
    ],
    then=[
        facts.is_large($thing, True)
    ]
)
def jompus_is_large(context, $thing):
    pass

@rule(
    foreach=[
        facts.is_a($thing, "jompus", True),
    ],
    then=[
        facts.is_a($thing, "wumpus", True)
    ]
)
def jompus_is_wumpus(context, $thing):
    pass

# Activate the knowledge base
engine.activate('rules')

# Query
query_result = facts.is_bright("Stella", True)