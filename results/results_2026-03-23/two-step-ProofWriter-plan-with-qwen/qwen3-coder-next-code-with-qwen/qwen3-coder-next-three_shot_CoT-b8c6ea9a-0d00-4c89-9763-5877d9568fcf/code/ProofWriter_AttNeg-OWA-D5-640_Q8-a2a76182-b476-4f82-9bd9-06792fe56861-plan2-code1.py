# Facts:
facts.is_rough(Bob, True)
facts.is_furry(Dave, True)
facts.is_nice(Dave, True)
facts.is_smart(Dave, True)
facts.is_red(Dave, False)
facts.is_green(Fiona, True)
facts.is_nice(Fiona, True)
facts.is_blue(Harry, True)
facts.is_furry(Harry, True)
facts.is_green(Harry, True)
facts.is_nice(Harry, True)
facts.is_red(Harry, False)
facts.is_rough(Harry, True)
facts.is_smart(Harry, True)

# Rules:
foreach facts.is_smart($thing, True) =>
    assert facts.is_green($thing, True)

foreach facts.is_nice($thing, True), facts.is_rough($thing, False) =>
    assert facts.is_red($thing, True)

foreach facts.is_nice($thing, True) =>
    assert facts.is_smart($thing, True)

foreach facts.is_rough($thing, True) =>
    assert facts.is_nice($thing, True)

foreach facts.is_blue($thing, True) =>
    assert facts.is_furry($thing, True)

foreach facts.is_blue($thing, True), facts.is_smart($thing, True) =>
    assert facts.is_furry($thing, True)

foreach facts.is_furry(Bob, True), facts.is_rough(Bob, False) =>
    assert facts.is_green(Bob, True)

foreach facts.is_green($thing, True) =>
    assert facts.is_blue($thing, True)

foreach facts.is_red($thing, True), facts.is_nice($thing, False) =>
    assert facts.is_blue($thing, False)

# Query:
facts.is_green(Bob, False)