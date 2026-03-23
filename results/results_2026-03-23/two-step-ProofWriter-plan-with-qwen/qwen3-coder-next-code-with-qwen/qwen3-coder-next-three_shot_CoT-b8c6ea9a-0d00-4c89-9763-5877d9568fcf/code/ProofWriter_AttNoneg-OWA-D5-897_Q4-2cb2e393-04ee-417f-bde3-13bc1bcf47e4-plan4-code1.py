# --- Knowledge Base Definition ---
knowledge_base:
    # --- Facts ---
    facts:
        is_nice("Anne")
        is_big("Bob")
        is_blue("Bob")
        is_cold("Bob")
        is_big("Charlie")
        is_cold("Charlie")
        is_nice("Charlie")
        is_young("Charlie")
        is_furry("Fiona")
        is_young("Fiona")

    # --- Rules ---
    rules:
        # If someone is furry and nice then they are cold
        foreach
            ?x is_furry(?x) and ?x is_nice(?x)
        then
            assert(is_cold(?x))

        # If Bob is blue and Bob is big then Bob is cold (redundant with general rule, but included)
        # This is already covered by the furry/nice -> cold rule? No, Bob isn't furry.
        # So we need this specific rule for Bob
        foreach
            is_blue("Bob") and is_big("Bob")
        then
            assert(is_cold("Bob"))

        # All blue, cold people are big
        foreach
            ?x is_blue(?x) and ?x is_cold(?x)
        then
            assert(is_big(?x))

        # If someone is nice then they are smart
        foreach
            ?x is_nice(?x)
        then
            assert(is_smart(?x))

        # All smart, big people are nice
        foreach
            ?x is_smart(?x) and ?x is_big(?x)
        then
            assert(is_nice(?x))

        # All smart people are blue
        foreach
            ?x is_smart(?x)
        then
            assert(is_blue(?x))

        # Blue, smart people are furry
        foreach
            ?x is_blue(?x) and ?x is_smart(?x)
        then
            assert(is_furry(?x))

        # Furry, cold people are smart
        foreach
            ?x is_furry(?x) and ?x is_cold(?x)
        then
            assert(is_smart(?x))

        # Cold people are big
        foreach
            ?x is_cold(?x)
        then
            assert(is_big(?x))

    # --- Query ---
    query:
        not is_smart("Charlie")