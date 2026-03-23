Facts:
is_big(Dave, True).
is_furry(Dave, True).
is_blue(Erin, True).
is_cold(Erin, True).
is_round(Erin, True).
is_quiet(Fiona, True).
is_rough(Gary, True).

Rules:
# If something is rough and cold then it is furry.
foreach
    is_rough($thing, True),
    is_cold($thing, True)
assert
    is_furry($thing, True).

# Quiet, big things are not round.
foreach
    is_quiet($thing, True),
    is_big($thing, True)
assert
    is_round($thing, False).

# If Dave is blue then Dave is furry.
foreach
    is_blue(Dave, True)
assert
    is_furry(Dave, True).

# All quiet, blue things are big.
foreach
    is_quiet($thing, True),
    is_blue($thing, True)
assert
    is_big($thing, True).

# If Fiona is furry then Fiona is blue.
foreach
    is_furry(Fiona, True)
assert
    is_blue(Fiona, True).

# If something is quiet then it is cold.
foreach
    is_quiet($thing, True)
assert
    is_cold($thing, True).

# All big things are cold.
foreach
    is_big($thing, True)
assert
    is_cold($thing, True).

# All blue, round things are not quiet.
foreach
    is_blue($thing, True),
    is_round($thing, True)
assert
    is_quiet($thing, False).

# Cold things are rough.
foreach
    is_cold($thing, True)
assert
    is_rough($thing, True).

Query:
is_furry(Erin, True).