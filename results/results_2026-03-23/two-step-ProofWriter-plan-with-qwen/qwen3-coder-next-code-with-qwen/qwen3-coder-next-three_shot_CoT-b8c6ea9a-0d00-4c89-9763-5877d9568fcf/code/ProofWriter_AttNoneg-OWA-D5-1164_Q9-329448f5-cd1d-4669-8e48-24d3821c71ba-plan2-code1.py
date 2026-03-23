# This is a PyKe knowledge base file (.krb format)
# Facts section
Facts:
    is_big(Bob)
    is_blue(Bob)
    is_cold(Bob)
    is_quiet(Bob)
    is_rough(Bob)
    is_smart(Bob)
    is_white(Bob)
    is_rough(Dave)
    is_blue(Fiona)
    is_big(Harry)
    is_cold(Harry)

# Rules section
Rules:
    # If someone is blue then they are cold.
    foreach is_blue($person)
        assert is_cold($person)

    # If someone is big then they are white.
    foreach is_big($person)
        assert is_white($person)

    # If Bob is rough and Bob is blue then Bob is big.
    foreach is_rough(Bob) and is_blue(Bob)
        assert is_big(Bob)

    # All blue, smart people are big.
    foreach is_blue($person) and is_smart($person)
        assert is_big($person)

    # If someone is blue and rough then they are quiet.
    foreach is_blue($person) and is_rough($person)
        assert is_quiet($person)

    # All smart people are blue.
    foreach is_smart($person)
        assert is_blue($person)

    # Cold people are rough.
    foreach is_cold($person)
        assert is_rough($person)

    # If someone is quiet then they are big.
    foreach is_quiet($person)
        assert is_big($person)

# Query section
Query:
    is_big(Fiona)