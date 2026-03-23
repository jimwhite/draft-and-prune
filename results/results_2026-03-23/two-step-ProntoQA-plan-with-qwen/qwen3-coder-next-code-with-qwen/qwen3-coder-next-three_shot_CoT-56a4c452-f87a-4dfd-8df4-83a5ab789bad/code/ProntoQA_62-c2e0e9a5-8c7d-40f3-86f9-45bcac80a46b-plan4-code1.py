# Facts:
Facts:
is_a(Wren, dumpus, True)

# Rules:
Rules:
foreach
    is_a($thing, zumpus, True)
assert
    is_nervous($thing, True)

foreach
    is_a($thing, zumpus, True)
assert
    is_a($thing, dumpus, True)

foreach
    is_a($thing, dumpus, True)
assert
    is_large($thing, True)

foreach
    is_a($thing, dumpus, True)
assert
    is_a($thing, rompus, True)

foreach
    is_a($thing, rompus, True)
assert
    is_brown($thing, True)

foreach
    is_a($thing, vumpus, True)
assert
    is_transparent($thing, True)

foreach
    is_a($thing, rompus, True)
assert
    is_a($thing, numpus, True)

foreach
    is_a($thing, numpus, True)
assert
    is_bitter($thing, False)

foreach
    is_a($thing, numpus, True)
assert
    is_a($thing, wumpus, True)

foreach
    is_a($thing, wumpus, True)
assert
    is_floral($thing, True)

foreach
    is_a($thing, wumpus, True)
assert
    is_a($thing, yumpus, True)

foreach
    is_a($thing, yumpus, True)
assert
    is_transparent($thing, False)

foreach
    is_a($thing, yumpus, True)
assert
    is_a($thing, tumpus, True)

foreach
    is_a($thing, tumpus, True)
assert
    is_bright($thing, False)

foreach
    is_a($thing, tumpus, True)
assert
    is_a($thing, impus, True)

# Query:
Query:
is_transparent(Wren, False)