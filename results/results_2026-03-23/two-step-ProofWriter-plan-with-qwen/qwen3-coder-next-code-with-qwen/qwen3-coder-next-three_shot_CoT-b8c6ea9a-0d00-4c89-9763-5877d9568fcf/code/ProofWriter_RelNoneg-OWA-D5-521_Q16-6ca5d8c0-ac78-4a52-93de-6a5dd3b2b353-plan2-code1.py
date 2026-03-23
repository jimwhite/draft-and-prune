Facts:
eats(cow, lion, True)
eats(lion, mouse, True)
needs(lion, mouse, True)
sees(mouse, lion, True)
eats(tiger, lion, True)
is_green(tiger, True)
is_red(tiger, True)
needs(tiger, lion, True)
needs(tiger, mouse, True)
sees(tiger, cow, True)

Rules:
foreach
    sees(person, lion, True)
assert
    is_cold(person, True)

foreach
    needs(person, tiger, True) and needs(person, mouse, True)
assert
    is_cold(person, True)

foreach
    needs(person, tiger, True) and eats(tiger, cow, True)
assert
    needs(tiger, lion, True)

foreach
    is_round(person, True)
assert
    is_green(person, True)

foreach
    is_young(person, True) and is_green(person, True)
assert
    is_round(person, True)

foreach
    eats(person, mouse, True) and sees(mouse, lion, True)
assert
    is_green(person, True)

foreach
    needs(person, tiger, True)
assert
    sees(tiger, lion, True)

foreach
    is_cold(person, True) and sees(person, lion, True)
assert
    needs(person, tiger, True)

Query:
needs(cow, tiger, True)