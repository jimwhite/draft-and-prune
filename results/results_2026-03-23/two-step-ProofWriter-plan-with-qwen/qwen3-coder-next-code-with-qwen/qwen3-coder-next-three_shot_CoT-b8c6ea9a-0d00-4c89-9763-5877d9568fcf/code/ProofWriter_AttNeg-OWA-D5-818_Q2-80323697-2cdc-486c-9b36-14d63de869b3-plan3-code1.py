# Facts:
Facts:
    is_young(Charlie, True)
    is_blue(Erin, True)
    is_kind(Erin, False)
    is_blue(Fiona, True)
    is_white(Fiona, True)
    is_blue(Gary, True)
    is_kind(Gary, True)

# Rules:
Rules:

# Rule: Furry, nice things are white.
    foreach
        is_furry(?thing, True)
        is_nice(?thing, True)
    assert
        is_white(?thing, True)

# Rule: If something is young and blue then it is smart.
    foreach
        is_young(?thing, True)
        is_blue(?thing, True)
    assert
        is_smart(?thing, True)

# Rule: All blue, smart things are furry.
    foreach
        is_blue(?thing, True)
        is_smart(?thing, True)
    assert
        is_furry(?thing, True)

# Rule: All smart, white things are furry.
    foreach
        is_smart(?thing, True)
        is_white(?thing, True)
    assert
        is_furry(?thing, True)

# Rule: Young things are nice.
    foreach
        is_young(?thing, True)
    assert
        is_nice(?thing, True)

# Rule: If Fiona is smart and Fiona is young then Fiona is not furry.
    foreach
        is_smart(Fiona, True)
        is_young(Fiona, True)
    assert
        is_furry(Fiona, False)

# Rule: If Erin is kind then Erin is furry.
    foreach
        is_kind(Erin, True)
    assert
        is_furry(Erin, True)

# Rule: If Gary is smart and Gary is white then Gary is not kind.
    foreach
        is_smart(Gary, True)
        is_white(Gary, True)
    assert
        is_kind(Gary, False)

# Rule: If something is nice then it is blue.
    foreach
        is_nice(?thing, True)
    assert
        is_blue(?thing, True)

# Query:
Query:
    is_white(Fiona, False)