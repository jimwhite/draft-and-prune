# PyKe program for the tumpus logic puzzle

from pyke import knowledge_engine

# Create knowledge engine instance
engine = knowledge_engine.engine(__name__)

# Facts section
Facts:
    ('is_a', 'Stella', 'yumpus')

# Rules section  
Rules:
    # Every tumpus is not angry
    foreach:
        is_a($thing, 'tumpus')
    assert:
        is_angry($thing, False)

    # Tumpuses are rompuses
    foreach:
        is_a($thing, 'tumpus')
    assert:
        is_a($thing, 'rompus')

    # Every numpus is not bright
    foreach:
        is_a($thing, 'numpus')
    assert:
        is_bright($thing, False)

    # Rompuses are not luminous
    foreach:
        is_a($thing, 'rompus')
    assert:
        is_luminous($thing, False)

    # Rompuses are yumpuses
    foreach:
        is_a($thing, 'rompus')
    assert:
        is_a($thing, 'yumpus')

    # Yumpuses are transparent
    foreach:
        is_a($thing, 'yumpus')
    assert:
        is_transparent($thing, True)

    # Yumpuses are zumpuses
    foreach:
        is_a($thing, 'yumpus')
    assert:
        is_a($thing, 'zumpus')

    # Each zumpus is not bitter
    foreach:
        is_a($thing, 'zumpus')
    assert:
        is_bitter($thing, False)

    # Zumpuses are impuses
    foreach:
        is_a($thing, 'zumpus')
    assert:
        is_a($thing, 'impus')

    # Impuses are red
    foreach:
        is_a($thing, 'impus')
    assert:
        is_red($thing, True)

    # Each impus is a dumpus
    foreach:
        is_a($thing, 'impus')
    assert:
        is_a($thing, 'dumpus')

    # Every dumpus is happy
    foreach:
        is_a($thing, 'dumpus')
    assert:
        is_happy($thing, True)

    # Each dumpus is a vumpus
    foreach:
        is_a($thing, 'dumpus')
    assert:
        is_a($thing, 'vumpus')

    # Vumpuses are bright
    foreach:
        is_a($thing, 'vumpus')
    assert:
        is_bright($thing, True)

    # Every vumpus is a jompus
    foreach:
        is_a($thing, 'vumpus')
    assert:
        is_a($thing, 'jompus')

    # Jompuses are large
    foreach:
        is_a($thing, 'jompus')
    assert:
        is_large($thing, True)

    # Each jompus is a wumpus
    foreach:
        is_a($thing, 'jompus')
    assert:
        is_a($thing, 'wumpus')

# Query section
Query:
    ('is_bright', 'Stella', True)