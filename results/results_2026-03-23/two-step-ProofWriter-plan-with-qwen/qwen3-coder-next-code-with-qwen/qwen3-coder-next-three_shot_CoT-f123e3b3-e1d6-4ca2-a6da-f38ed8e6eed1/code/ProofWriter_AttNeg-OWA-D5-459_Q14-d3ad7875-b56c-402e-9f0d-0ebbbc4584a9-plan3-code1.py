```python
# PyKe program: Gary is white?

# --- Facts ---
is_cold("Bob", False)
is_furry("Bob", True)
is_round("Bob", True)

is_big("Charlie", True)
is_furry("Charlie", True)
is_quiet("Charlie", True)
is_red("Charlie", True)
is_white("Charlie", False)

is_big("Erin", True)

is_big("Gary", True)
is_quiet("Gary", True)

# --- Rules ---
# Rule: If someone is red and cold then they are furry.
red_and_cold_are_furry
    foreach
        is_red($person, True)
        is_cold($person, True)
    assert
        is_furry($person, True)

# Rule: All furry people are round.
furry_are_round
    foreach
        is_furry($person, True)
    assert
        is_round($person, True)

# Rule: Big people are red.
big_are_red
    foreach
        is_big($person, True)
    assert
        is_red($person, True)

# Rule: Round people are quiet.
round_are_quiet
    foreach
        is_round($person, True)
    assert
        is_quiet($person, True)

# Rule: If someone is red then they are cold.
red_are_cold
    foreach
        is_red($person, True)
    assert
        is_cold($person, True)

# --- Query ---
is_white("Gary", True)
```