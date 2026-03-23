facts:
is_big(Bob, True)
is_blue(Bob, True)
is_cold(Bob, True)
is_quiet(Bob, True)
is_rough(Bob, True)
is_smart(Bob, True)
is_white(Bob, True)

is_rough(Dave, True)

is_blue(Fiona, True)

is_big(Harry, True)
is_cold(Harry, True)

rules:
# Rule: If someone is blue then they are cold.
blue_to_cold:
    foreach
        is_blue($person, True)
    assert
        is_cold($person, True)

# Rule: If someone is big then they are white.
big_to_white:
    foreach
        is_big($person, True)
    assert
        is_white($person, True)

# Rule: If Bob is rough and Bob is blue then Bob is big.
bob_rough_blue_to_big:
    foreach
        is_rough(Bob, True)
        is_blue(Bob, True)
    assert
        is_big(Bob, True)

# Rule: All blue, smart people are big.
blue_smart_to_big:
    foreach
        is_blue($person, True)
        is_smart($person, True)
    assert
        is_big($person, True)

# Rule: If someone is blue and rough then they are quiet.
blue_rough_to_quiet:
    foreach
        is_blue($person, True)
        is_rough($person, True)
    assert
        is_quiet($person, True)

# Rule: All smart people are blue.
smart_to_blue:
    foreach
        is_smart($person, True)
    assert
        is_blue($person, True)

# Rule: Cold people are rough.
cold_to_rough:
    foreach
        is_cold($person, True)
    assert
        is_rough($person, True)

# Rule: If someone is quiet then they are big.
quiet_to_big:
    foreach
        is_quiet($person, True)
    assert
        is_big($person, True)

query:
is_big(Fiona, True)