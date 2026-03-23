from pyke import knowledge_engine

# Initialize knowledge engine
engine = knowledge_engine.engine(__file__)

# Facts
engine.add_universal_fact('facts', 'is_a', 'Stella', 'yumpus', True)

# Rules
@engine.rule
def tumpus_is_rompus():
    return (
        ('facts', 'is_a', '$thing', 'tumpus', True),
        (),
        (('facts', 'is_a', '$thing', 'rompus', True),)
    )

@engine.rule
def rompus_is_yumpus():
    return (
        ('facts', 'is_a', '$thing', 'rompus', True),
        (),
        (('facts', 'is_a', '$thing', 'yumpus', True),)
    )

@engine.rule
def yumpus_is_zumpus():
    return (
        ('facts', 'is_a', '$thing', 'yumpus', True),
        (),
        (('facts', 'is_a', '$thing', 'zumpus', True),)
    )

@engine.rule
def zumpus_is_impus():
    return (
        ('facts', 'is_a', '$thing', 'zumpus', True),
        (),
        (('facts', 'is_a', '$thing', 'impus', True),)
    )

@engine.rule
def impus_is_dumpus():
    return (
        ('facts', 'is_a', '$thing', 'impus', True),
        (),
        (('facts', 'is_a', '$thing', 'dumpus', True),)
    )

@engine.rule
def dumpus_is_vumpus():
    return (
        ('facts', 'is_a', '$thing', 'dumpus', True),
        (),
        (('facts', 'is_a', '$thing', 'vumpus', True),)
    )

@engine.rule
def vumpus_is_bright():
    return (
        ('facts', 'is_a', '$thing', 'vumpus', True),
        (),
        (('facts', 'is_bright', '$thing', True),)
    )

# Additional rules for completeness (though not needed for this specific query)
@engine.rule
def tumpus_is_not_angry():
    return (
        ('facts', 'is_a', '$thing', 'tumpus', True),
        (),
        (('facts', 'is_angry', '$thing', False),)
    )

@engine.rule
def numpus_is_not_bright():
    return (
        ('facts', 'is_a', '$thing', 'numpus', True),
        (),
        (('facts', 'is_bright', '$thing', False),)
    )

@engine.rule
def rompus_is_not_luminous():
    return (
        ('facts', 'is_a', '$thing', 'rompus', True),
        (),
        (('facts', 'is_luminous', '$thing', False),)
    )

@engine.rule
def yumpus_is_transparent():
    return (
        ('facts', 'is_a', '$thing', 'yumpus', True),
        (),
        (('facts', 'is_transparent', '$thing', True),)
    )

@engine.rule
def zumpus_is_not_bitter():
    return (
        ('facts', 'is_a', '$thing', 'zumpus', True),
        (),
        (('facts', 'is_bitter', '$thing', False),)
    )

@engine.rule
def impus_is_red():
    return (
        ('facts', 'is_a', '$thing', 'impus', True),
        (),
        (('facts', 'is_red', '$thing', True),)
    )

@engine.rule
def dumpus_is_happy():
    return (
        ('facts', 'is_a', '$thing', 'dumpus', True),
        (),
        (('facts', 'is_happy', '$thing', True),)
    )

@engine.rule
def vumpus_is_jompus():
    return (
        ('facts', 'is_a', '$thing', 'vumpus', True),
        (),
        (('facts', 'is_a', '$thing', 'jompus', True),)
    )

@engine.rule
def jompus_is_large():
    return (
        ('facts', 'is_a', '$thing', 'jompus', True),
        (),
        (('facts', 'is_large', '$thing', True),)
    )

@engine.rule
def jompus_is_wumpus():
    return (
        ('facts', 'is_a', '$thing', 'jompus', True),
        (),
        (('facts', 'is_a', '$thing', 'wumpus', True),)
    )

# Build the engine
engine.build()

# Query: Is Stella bright?
result = engine.query().facts.is_bright('Stella', True).get()

# Output the result
print("Stella is bright:", bool(result))