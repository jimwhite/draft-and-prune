# Facts section
Facts:
is_big(Dave, True)
is_furry(Dave, True)
is_blue(Erin, True)
is_cold(Erin, True)
is_round(Erin, True)
is_quiet(Fiona, True)
is_rough(Gary, True)

# Rules section
Rules:
# If something is rough and cold then it is furry.
is_furry(X, True) :-
    is_rough(X, True),
    is_cold(X, True)

# Quiet, big things are not round.
is_round(X, False) :-
    is_quiet(X, True),
    is_big(X, True)

# If Dave is blue then Dave is furry.
is_furry(Dave, True) :-
    is_blue(Dave, True)

# All quiet, blue things are big.
is_big(X, True) :-
    is_quiet(X, True),
    is_blue(X, True)

# If Fiona is furry then Fiona is blue.
is_blue(Fiona, True) :-
    is_furry(Fiona, True)

# If something is quiet then it is cold.
is_cold(X, True) :-
    is_quiet(X, True)

# All big things are cold.
is_cold(X, True) :-
    is_big(X, True)

# All blue, round things are not quiet.
is_quiet(X, False) :-
    is_blue(X, True),
    is_round(X, True)

# Cold things are rough.
is_rough(X, True) :-
    is_cold(X, True)

# Query section
Query:
is_furry(Erin, True)