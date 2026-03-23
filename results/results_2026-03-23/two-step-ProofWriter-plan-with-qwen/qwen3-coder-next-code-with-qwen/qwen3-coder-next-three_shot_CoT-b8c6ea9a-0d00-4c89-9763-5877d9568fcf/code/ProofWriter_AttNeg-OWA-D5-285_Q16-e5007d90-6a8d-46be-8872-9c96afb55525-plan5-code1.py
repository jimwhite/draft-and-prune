# --- Facts ---
facts:
is_big("Bob", True)
is_cold("Bob", True)
is_furry("Bob", True)
is_smart("Bob", True)

is_cold("Fiona", True)
is_green("Fiona", False)
is_white("Fiona", True)

is_smart("Gary", True)

is_big("Harry", True)
is_cold("Harry", True)
is_smart("Harry", True)

# --- Rules ---
rules:
foreach
    ?person is_green(?person, True)
assert
    is_furry(?person, True)

foreach
    ?person is_smart(?person, True)
assert
    is_green(?person, True)

foreach
    ?person is_big(?person, True)
assert
    is_cold(?person, True)

foreach
    ?person is_smart(?person, True)
    ?person is_furry(?person, True)
assert
    is_big(?person, True)

foreach
    ?person is_cold(?person, True)
assert
    is_blue(?person, False)

foreach
    ?person is_white(?person, True)
    ?person is_cold(?person, False)
assert
    is_blue(?person, False)

foreach
    ?person is_green(?person, False)
    ?person is_white(?person, False)
assert
    is_furry(?person, True)

# --- Query ---
query:
is_white("Bob", True)