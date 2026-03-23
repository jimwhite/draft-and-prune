facts:
is_big("Bob", True)
is_blue("Bob", True)
is_cold("Bob", True)
is_quiet("Bob", True)
is_rough("Bob", True)
is_smart("Bob", True)
is_white("Bob", True)

is_rough("Dave", True)

is_blue("Fiona", True)

is_big("Harry", True)
is_cold("Harry", True)

rules:
# Rule: If someone is blue then they are cold.
foreach
    facts.is_blue($person, True)
assert
    facts.is_cold($person, True)

# Rule: If someone is big then they are white.
foreach
    facts.is_big($person, True)
assert
    facts.is_white($person, True)

# Rule: If Bob is rough and Bob is blue then Bob is big.
foreach
    facts.is_rough("Bob", True)
    facts.is_blue("Bob", True)
assert
    facts.is_big("Bob", True)

# Rule: All blue, smart people are big.
foreach
    facts.is_blue($person, True)
    facts.is_smart($person, True)
assert
    facts.is_big($person, True)

# Rule: If someone is blue and rough then they are quiet.
foreach
    facts.is_blue($person, True)
    facts.is_rough($person, True)
assert
    facts.is_quiet($person, True)

# Rule: All smart people are blue.
foreach
    facts.is_smart($person, True)
assert
    facts.is_blue($person, True)

# Rule: Cold people are rough.
foreach
    facts.is_cold($person, True)
assert
    facts.is_rough($person, True)

# Rule: If someone is quiet then they are big.
foreach
    facts.is_quiet($person, True)
assert
    facts.is_big($person, True)

query:
facts.is_big("Fiona", True)