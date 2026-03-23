# --- Facts ---
facts:
is_young("Charlie", True)
is_blue("Erin", True)
is_kind("Erin", False)
is_blue("Fiona", True)
is_white("Fiona", True)
is_blue("Gary", True)
is_kind("Gary", True)

# --- Rules ---
rules:
# Furry, nice things are white.
foreach
    $x is furry($x)
    $x is nice($x)
assert
    $x is white($x)

# If something is young and blue then it is smart.
foreach
    $x is young($x)
    $x is blue($x)
assert
    $x is smart($x)

# All blue, smart things are furry.
foreach
    $x is blue($x)
    $x is smart($x)
assert
    $x is furry($x)

# All smart, white things are furry.
foreach
    $x is smart($x)
    $x is white($x)
assert
    $x is furry($x)

# Young things are nice.
foreach
    $x is young($x)
assert
    $x is nice($x)

# If Fiona is smart and Fiona is young then Fiona is not furry.
foreach
    $x == "Fiona"
    $x is smart($x)
    $x is young($x)
assert
    not_furry($x)

# If Erin is kind then Erin is furry.
foreach
    $x == "Erin"
    $x is kind($x)
assert
    $x is furry($x)

# If Gary is smart and Gary is white then Gary is not kind.
foreach
    $x == "Gary"
    $x is smart($x)
    $x is white($x)
assert
    not_kind($x)

# If something is nice then it is blue.
foreach
    $x is nice($x)
assert
    $x is blue($x)

# --- Query ---
query:
is_white("Fiona", False)