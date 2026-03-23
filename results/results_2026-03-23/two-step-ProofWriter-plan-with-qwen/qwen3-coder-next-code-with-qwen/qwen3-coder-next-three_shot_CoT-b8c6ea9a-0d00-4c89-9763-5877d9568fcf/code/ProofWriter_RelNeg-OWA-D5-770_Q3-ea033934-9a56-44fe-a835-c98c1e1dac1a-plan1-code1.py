Facts:
chases(bald_eagle, cat, True)
is_young(bald_eagle, True)
is_rough(cat, True)
is_young(cat, True)
sees(cat, bald_eagle, True)
chases(lion, bald_eagle, True)
chases(lion, cat, True)
eats(lion, bald_eagle, True)
eats(lion, cat, True)
chases(mouse, bald_eagle, True)
chases(mouse, lion, True)
eats(mouse, bald_eagle, True)
is_young(mouse, True)

Rules:
foreach
    is_kind($thing, True)
assert
    is_round($thing, True)

foreach
    chases($thing, bald_eagle, True)
assert
    is_round($thing, True)

foreach
    is_round($thing, True)
assert
    sees($thing, bald_eagle, True)

foreach
    chases($thing, cat, True)
    chases(cat, bald_eagle, True)
assert
    eats($thing, bald_eagle, True)

foreach
    chases($thing, cat, True)
assert
    sees(cat, lion, True)

foreach
    sees($thing, cat, True)
assert
    chases($thing, bald_eagle, True)

foreach
    is_young(bald_eagle, True)
    chases(bald_eagle, lion, True)
assert
    sees(bald_eagle, lion, True)

foreach
    eats(mouse, cat, True)
    eats(mouse, bald_eagle, True)
assert
    eats(bald_eagle, cat, True)

foreach
    sees($thing, bald_eagle, True)
    chases($thing, cat, True)
assert
    sees(bald_eagle, cat, True)

Query:
sees(cat, lion, True)