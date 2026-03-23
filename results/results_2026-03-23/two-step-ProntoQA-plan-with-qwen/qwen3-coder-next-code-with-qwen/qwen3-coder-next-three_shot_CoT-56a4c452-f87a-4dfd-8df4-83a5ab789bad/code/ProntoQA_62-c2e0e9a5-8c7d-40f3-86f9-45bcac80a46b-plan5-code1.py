Facts:
is_a(Wren, dumpus, True)

Rules:
# Zumpus rules
foreach is_a(?x, zumpus)
    => assert is_nervous(?x)

foreach is_a(?x, zumpus)
    => assert is_a(?x, dumpus)

# Dumpus rules
foreach is_a(?x, dumpus)
    => assert is_large(?x)

foreach is_a(?x, dumpus)
    => assert is_a(?x, rompus)

# Rompus rules
foreach is_a(?x, rompus)
    => assert is_brown(?x)

foreach is_a(?x, rompus)
    => assert is_a(?x, numpus)

# Vumpus rule
foreach is_a(?x, vumpus)
    => assert is_transparent(?x)

# Numpus rules
foreach is_a(?x, numpus)
    => assert not(is_bitter(?x))

foreach is_a(?x, numpus)
    => assert is_a(?x, wumpus)

# Wumpus rules
foreach is_a(?x, wumpus)
    => assert is_floral(?x)

foreach is_a(?x, wumpus)
    => assert is_a(?x, yumpus)

# Yumpus rules
foreach is_a(?x, yumpus)
    => assert not(is_transparent(?x))

foreach is_a(?x, yumpus)
    => assert is_a(?x, tumpus)

# Tumpus rules
foreach is_a(?x, tumpus)
    => assert not(is_bright(?x))

foreach is_a(?x, tumpus)
    => assert is_a(?x, impus)

Query:
not(is_transparent(Wren))