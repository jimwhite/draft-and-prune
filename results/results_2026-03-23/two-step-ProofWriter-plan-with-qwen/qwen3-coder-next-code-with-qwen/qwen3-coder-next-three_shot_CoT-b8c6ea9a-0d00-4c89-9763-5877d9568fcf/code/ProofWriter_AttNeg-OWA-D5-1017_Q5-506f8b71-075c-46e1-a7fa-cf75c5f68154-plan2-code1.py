# PyKe Program: Furry Inference Problem

from pyke import knowledge_engine, facts, rules

engine = knowledge_engine.engine(__file__)

facts:
    is_big("Dave", True)
    is_furry("Dave", True)
    is_blue("Erin", True)
    is_cold("Erin", True)
    is_round("Erin", True)
    is_quiet("Fiona", True)
    is_rough("Gary", True)

rules:
    # If something is rough and cold then it is furry.
    foreach
        is_rough(?x, True),
        is_cold(?x, True)
    do
        assert(is_furry(?x, True))

    # Quiet, big things are not round.
    foreach
        is_quiet(?x, True),
        is_big(?x, True)
    do
        assert(is_round(?x, False))

    # If Dave is blue then Dave is furry.
    foreach
        is_blue("Dave", True)
    do
        assert(is_furry("Dave", True))

    # All quiet, blue things are big.
    foreach
        is_quiet(?x, True),
        is_blue(?x, True)
    do
        assert(is_big(?x, True))

    # If Fiona is furry then Fiona is blue.
    foreach
        is_furry("Fiona", True)
    do
        assert(is_blue("Fiona", True))

    # If something is quiet then it is cold.
    foreach
        is_quiet(?x, True)
    do
        assert(is_cold(?x, True))

    # All big things are cold.
    foreach
        is_big(?x, True)
    do
        assert(is_cold(?x, True))

    # All blue, round things are not quiet.
    foreach
        is_blue(?x, True),
        is_round(?x, True)
    do
        assert(is_quiet(?x, False))

    # Cold things are rough.
    foreach
        is_cold(?x, True)
    do
        assert(is_rough(?x, True))

query:
    is_furry("Erin", True)