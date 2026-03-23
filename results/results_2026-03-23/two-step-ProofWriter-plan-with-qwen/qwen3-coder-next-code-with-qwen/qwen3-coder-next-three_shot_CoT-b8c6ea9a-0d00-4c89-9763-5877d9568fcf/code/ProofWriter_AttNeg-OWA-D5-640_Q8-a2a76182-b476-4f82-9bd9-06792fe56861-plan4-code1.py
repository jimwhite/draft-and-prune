Facts:
    is_rough(Bob, True)
    is_furry(Dave, True)
    is_nice(Dave, True)
    is_red(Dave, False)
    is_smart(Dave, True)
    is_green(Fiona, True)
    is_nice(Fiona, True)
    is_blue(Harry, True)
    is_furry(Harry, True)
    is_green(Harry, True)
    is_nice(Harry, True)
    is_red(Harry, False)
    is_rough(Harry, True)
    is_smart(Harry, True)

Rules:
    # Smart things are green.
    foreach
        facts.is_smart($thing, True)
    assert
        facts.is_green($thing, True)

    # If something is nice and not rough then it is red.
    foreach
        facts.is_nice($thing, True)
        facts.is_rough($thing, False)
    assert
        facts.is_red($thing, True)

    # If something is nice then it is smart.
    foreach
        facts.is_nice($thing, True)
    assert
        facts.is_smart($thing, True)

    # If something is rough then it is nice.
    foreach
        facts.is_rough($thing, True)
    assert
        facts.is_nice($thing, True)

    # If something is blue then it is furry.
    foreach
        facts.is_blue($thing, True)
    assert
        facts.is_furry($thing, True)

    # All blue, smart things are furry.
    foreach
        facts.is_blue($thing, True)
        facts.is_smart($thing, True)
    assert
        facts.is_furry($thing, True)

    # If Bob is furry and Bob is not rough then Bob is green.
    foreach
        facts.is_furry(Bob, True)
        facts.is_rough(Bob, False)
    assert
        facts.is_green(Bob, True)

    # If something is green then it is blue.
    foreach
        facts.is_green($thing, True)
    assert
        facts.is_blue($thing, True)

    # If something is red and not nice then it is not blue.
    foreach
        facts.is_red($thing, True)
        facts.is_nice($thing, False)
    assert
        facts.is_blue($thing, False)

Query:
    facts.is_green(Bob, False)