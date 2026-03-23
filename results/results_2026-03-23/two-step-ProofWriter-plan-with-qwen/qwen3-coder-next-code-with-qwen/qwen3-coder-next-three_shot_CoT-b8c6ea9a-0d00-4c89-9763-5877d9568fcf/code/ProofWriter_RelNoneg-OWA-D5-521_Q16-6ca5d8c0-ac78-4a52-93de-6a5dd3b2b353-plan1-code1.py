facts:
eats(cow, lion, True).
eats(lion, mouse, True).
eats(tiger, lion, True).
needs(lion, mouse, True).
sees(mouse, lion, True).
is_green(tiger, True).
is_red(tiger, True).
needs(tiger, lion, True).
needs(tiger, mouse, True).
sees(tiger, cow, True).

rules:
# If someone sees the lion then they are cold.
rule1:
    foreach
        sees(?x, lion, True)
    assert
        is_cold(?x, True)

# If someone needs the tiger and they need the mouse then they are cold.
rule2:
    foreach
        needs(?x, tiger, True)
        needs(?x, mouse, True)
    assert
        is_cold(?x, True)

# If someone needs the tiger and the tiger eats the cow then the tiger needs the lion.
rule3:
    foreach
        needs(?x, tiger, True)
        eats(tiger, cow, True)
    assert
        needs(tiger, lion, True)

# All round people are green.
rule4:
    foreach
        is_round(?x, True)
    assert
        is_green(?x, True)

# All young, green people are round.
rule5:
    foreach
        is_young(?x, True)
        is_green(?x, True)
    assert
        is_round(?x, True)

# If someone eats the mouse and the mouse sees the lion then they are green.
rule6:
    foreach
        eats(?x, mouse, True)
        sees(mouse, lion, True)
    assert
        is_green(?x, True)

# If someone needs the tiger then the tiger sees the lion.
rule7:
    foreach
        needs(?x, tiger, True)
    assert
        sees(tiger, lion, True)

# If someone is cold and they see the lion then they need the tiger.
rule8:
    foreach
        is_cold(?x, True)
        sees(?x, lion, True)
    assert
        needs(?x, tiger, True)

query:
needs(cow, tiger, True)