Facts:
is_rough(Bob)
is_furry(Dave)
is_nice(Dave)
not_red(Dave)
is_smart(Dave)
is_green(Fiona)
is_nice(Fiona)
is_blue(Harry)
is_furry(Harry)
is_green(Harry)
is_nice(Harry)
not_red(Harry)
is_rough(Harry)
is_smart(Harry)

Rules:
# Smart things are green.
foreach is_smart($x)
    assert is_green($x)

# If something is nice and not rough then it is red.
foreach is_nice($x)
    and not is_rough($x)
    assert is_red($x)

# If something is nice then it is smart.
foreach is_nice($x)
    assert is_smart($x)

# If something is rough then it is nice.
foreach is_rough($x)
    assert is_nice($x)

# If something is blue then it is furry.
foreach is_blue($x)
    assert is_furry($x)

# All blue, smart things are furry.
foreach is_blue($x)
    and is_smart($x)
    assert is_furry($x)

# If Bob is furry and Bob is not rough then Bob is green.
foreach is_furry(Bob)
    and not is_rough(Bob)
    assert is_green(Bob)

# If something is green then it is blue.
foreach is_green($x)
    assert is_blue($x)

# If something is red and not nice then it is not blue.
foreach is_red($x)
    and not is_nice($x)
    assert not_blue($x)

Query:
not_green(Bob)