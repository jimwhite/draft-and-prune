# Facts:
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

# Rules:
Rules:
smart_are_green: foreach
    facts.is_smart($x, True)
assert
    facts.is_green($x, True)

nice_and_not_rough_is_red: foreach
    facts.is_nice($x, True)
    facts.is_rough($x, False)
assert
    facts.is_red($x, True)

nice_are_smart: foreach
    facts.is_nice($x, True)
assert
    facts.is_smart($x, True)

rough_are_nice: foreach
    facts.is_rough($x, True)
assert
    facts.is_nice($x, True)

blue_are_furry: foreach
    facts.is_blue($x, True)
assert
    facts.is_furry($x, True)

blue_and_smart_are_furry: foreach
    facts.is_blue($x, True)
    facts.is_smart($x, True)
assert
    facts.is_furry($x, True)

bob_furry_and_not_rough_is_green: foreach
    facts.is_furry(Bob, True)
    facts.is_rough(Bob, False)
assert
    facts.is_green(Bob, True)

green_are_blue: foreach
    facts.is_green($x, True)
assert
    facts.is_blue($x, True)

red_and_not_nice_is_not_blue: foreach
    facts.is_red($x, True)
    facts.is_nice($x, False)
assert
    facts.is_blue($x, False)

# Query:
Query:
facts.is_green(Bob, True)