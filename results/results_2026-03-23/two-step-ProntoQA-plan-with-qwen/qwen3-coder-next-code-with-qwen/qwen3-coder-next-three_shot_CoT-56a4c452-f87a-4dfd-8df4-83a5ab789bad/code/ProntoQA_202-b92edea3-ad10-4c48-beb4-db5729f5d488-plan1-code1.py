# PyKe program for tumpus logic puzzle

"""
facts:
is_a(Wren, zumpus).
"""

"""
rules:
# Tumpuses are temperate.
tumpus_is_temperate <- is_a($X, tumpus).

# Tumpuses are impuses.
is_a($X, impus) <- is_a($X, tumpus).

# Every impus is orange.
is_orange($X) <- is_a($X, impus).

# Impuses are yumpuses.
is_a($X, yumpus) <- is_a($X, impus).

# Each yumpus is shy.
is_shy($X) <- is_a($X, yumpus).

# Yumpuses are zumpuses.
is_a($X, zumpus) <- is_a($X, yumpus).

# Zumpuses are bright.
is_bright($X) <- is_a($X, zumpus).

# Every zumpus is a rompus.
is_a($X, rompus) <- is_a($X, zumpus).

# Every numpus is opaque.
is_opaque($X) <- is_a($X, numpus).

# Rompuses are small.
is_small($X) <- is_a($X, rompus).

# Every rompus is a dumpus.
is_a($X, dumpus) <- is_a($X, rompus).

# Dumpuses are not floral.
not(is_floral($X)) <- is_a($X, dumpus).

# Each dumpus is a wumpus.
is_a($X, wumpus) <- is_a($X, dumpus).

# Each wumpus is aggressive.
is_aggressive($X) <- is_a($X, wumpus).

# Wumpuses are vumpuses.
is_a($X, vumpus) <- is_a($X, wumpus).

# Each vumpus is not opaque.
not(is_opaque($X)) <- is_a($X, vumpus).

# Every vumpus is a jompus.
is_a($X, jompus) <- is_a($X, vumpus).
"""

"""
query:
not(is_opaque(Wren)).
"""