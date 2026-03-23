Facts:
is_big(Charlie, True)
is_cold(Charlie, True)
is_nice(Charlie, True)
is_young(Charlie, True)

Rules:
forall person:
    is_furry(person, True) ∧ is_nice(person, True) → is_cold(person, True)

is_blue(Bob, True) ∧ is_big(Bob, True) → is_cold(Bob, True)

forall person:
    is_blue(person, True) ∧ is_cold(person, True) → is_big(person, True)

forall person:
    is_nice(person, True) → is_smart(person, True)

forall person:
    is_smart(person, True) ∧ is_big(person, True) → is_nice(person, True)

forall person:
    is_smart(person, True) → is_blue(person, True)

forall person:
    is_blue(person, True) ∧ is_smart(person, True) → is_furry(person, True)

forall person:
    is_furry(person, True) ∧ is_cold(person, True) → is_smart(person, True)

forall person:
    is_cold(person, True) → is_big(person, True)

Query:
is_smart(Charlie, False)