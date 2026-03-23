facts:
eats(cow, lion, True).
eats(lion, mouse, True).
eats(tiger, lion, True).
needs(lion, mouse, True).
needs(tiger, lion, True).
needs(tiger, mouse, True).
sees(mouse, lion, True).
sees(tiger, cow, True).
is_green(tiger, True).
is_red(tiger, True).

rules:
# If someone sees the lion then they are cold.
rule1:
    foreach
        sees(X, lion, True)
    assert
        is_cold(X, True)

# If someone needs the tiger and they need the mouse then they are cold.
rule2:
    foreach
        needs(X, tiger, True)
        needs(X, mouse, True)
    assert
        is_cold(X, True)

# If someone needs the tiger and the tiger eats the cow then the tiger needs the lion.
rule3:
    foreach
        needs(X, tiger, True)
        eats(tiger, cow, True)
    assert
        needs(tiger, lion, True)

# All round people are green.
rule4:
    foreach
        is_round(X, True)
    assert
        is_green(X, True)

# All young, green people are round.
rule5:
    foreach
        is_young(X, True)
        is_green(X, True)
    assert
        is_round(X, True)

# If someone eats the mouse and the mouse sees the lion then they are green.
rule6:
    foreach
        eats(X, mouse, True)
        sees(mouse, lion, True)
    assert
        is_green(X, True)

# If someone needs the tiger then the tiger sees the lion.
rule7:
    foreach
        needs(X, tiger, True)
    assert
        sees(tiger, lion, True)

# If someone is cold and they see the lion then they need the tiger.
rule8:
    foreach
        is_cold(X, True)
        sees(X, lion, True)
    assert
        needs(X, tiger, True)

query:
check(needs(cow, tiger, True))