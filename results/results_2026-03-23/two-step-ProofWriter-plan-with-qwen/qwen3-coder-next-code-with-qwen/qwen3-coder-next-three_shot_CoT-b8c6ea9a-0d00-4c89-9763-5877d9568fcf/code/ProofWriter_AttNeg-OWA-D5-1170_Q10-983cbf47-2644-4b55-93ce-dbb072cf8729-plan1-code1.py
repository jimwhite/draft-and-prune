from pyke import knowledge_engine

engine = knowledge_engine.engine(__file__)

facts:
    is_kind("Bob", True)
    is_quiet("Charlie", True)
    is_rough("Charlie", True)
    is_kind("Fiona", True)
    is_rough("Fiona", True)
    is_white("Fiona", True)
    is_nice("Gary", True)

rules:
    # If Gary is red and Gary is white then Gary is quiet.
    rule gary_red_white_to_quiet:
        foreach
            is_red(?x, True)
            is_white(?x, True)
        then
            assert(is_quiet(?x, True))

    # All white things are rough.
    rule all_white_are_rough:
        foreach
            is_white(?x, True)
        then
            assert(is_rough(?x, True))

    # If something is rough then it is red.
    rule rough_to_red:
        foreach
            is_rough(?x, True)
        then
            assert(is_red(?x, True))

    # If something is nice then it is white.
    rule nice_to_white:
        foreach
            is_nice(?x, True)
        then
            assert(is_white(?x, True))

    # All smart things are white.
    rule smart_to_white:
        foreach
            is_smart(?x, True)
        then
            assert(is_white(?x, True))

    # Rough, quiet things are not kind.
    rule rough_quiet_not_kind:
        foreach
            is_rough(?x, True)
            is_quiet(?x, True)
        then
            assert(is_kind(?x, False))

    # If something is quiet and not smart then it is kind.
    rule quiet_not_smart_to_kind:
        foreach
            is_quiet(?x, True)
            is_smart(?x, False)
        then
            assert(is_kind(?x, True))

    # Smart things are quiet.
    rule smart_to_quiet:
        foreach
            is_smart(?x, True)
        then
            assert(is_quiet(?x, True))

    # If something is smart and not rough then it is quiet.
    rule smart_not_rough_to_quiet:
        foreach
            is_smart(?x, True)
            is_rough(?x, False)
        then
            assert(is_quiet(?x, True))

query:
    is_quiet("Gary", False)