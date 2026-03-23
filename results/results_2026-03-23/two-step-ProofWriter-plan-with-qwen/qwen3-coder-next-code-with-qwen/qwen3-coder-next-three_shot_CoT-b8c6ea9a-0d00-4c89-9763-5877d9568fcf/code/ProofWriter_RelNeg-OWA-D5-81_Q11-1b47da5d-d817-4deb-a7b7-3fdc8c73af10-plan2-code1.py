facts:
eats("cat", "squirrel", True)
sees("cat", "squirrel", True)
eats("cow", "squirrel", True)
sees("cow", "cat", True)
is_round("rabbit", True)
sees("rabbit", "cat", True)
eats("squirrel", "rabbit", True)
is_cold("squirrel", True)
needs("squirrel", "rabbit", True)
sees("squirrel", "cat", True)

rules:
foreach
    sees(X, "cat")
    not is_green(X)
assert
    sees(X, "cow")

foreach
    is_kind("rabbit")
    sees("rabbit", X)
    X = "squirrel"
assert
    needs("squirrel", "rabbit")

foreach
    is_rough(X)
assert
    is_cold(X)

foreach
    sees(X, "rabbit")
assert
    not is_round(X)

foreach
    sees(X, "squirrel")
    not is_green(X)
assert
    needs(X, "squirrel")

foreach
    eats(X, "cow")
assert
    sees(X, "rabbit")

foreach
    eats(X, "squirrel")
assert
    is_rough(X)

foreach
    is_cold(X)
assert
    eats(X, "cow")

query:
is_round("cat", False)