# -*- mode: python; -*-
# PyKe facts, rules, and query for the logic puzzle

'''
Facts:
is_cold(Bob)
is_quiet(Bob)
is_red(Bob)
is_smart(Bob)

is_kind(Charlie)
is_quiet(Charlie)
is_red(Charlie)
is_rough(Charlie)

is_cold(Dave)
is_kind(Dave)
is_smart(Dave)

is_quiet(Fiona)

Rules:
# If something is quiet and cold then it is smart.
foreach
    is_quiet(?x)
    is_cold(?x)
assert
    is_smart(?x)

# Red, cold things are round.
foreach
    is_red(?x)
    is_cold(?x)
assert
    is_round(?x)

# If something is kind and rough then it is red.
foreach
    is_kind(?x)
    is_rough(?x)
assert
    is_red(?x)

# All quiet things are rough.
foreach
    is_quiet(?x)
assert
    is_rough(?x)

# Cold, smart things are red.
foreach
    is_cold(?x)
    is_smart(?x)
assert
    is_red(?x)

# If something is rough then it is cold.
foreach
    is_rough(?x)
assert
    is_cold(?x)

# All red things are rough.
foreach
    is_red(?x)
assert
    is_rough(?x)

# If Dave is smart and Dave is kind then Dave is quiet.
foreach
    is_smart(Dave)
    is_kind(Dave)
assert
    is_quiet(Dave)

Query:
is_kind(Charlie)
'''