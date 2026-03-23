facts:
furry(Anne, True).
furry(Bob, True).
furry(Gary, True).
blue(Gary, True).
blue(Harry, True).
cold(Gary, True).
cold(Harry, True).
quiet(Gary, True).
quiet(Harry, True).
round(Gary, True).
round(Harry, True).
young(Harry, True).

rules:
# Rule: Cold, blue things are quiet.
foreach
    cold(?x, True),
    blue(?x, True)
assert
    quiet(?x, True).

# Rule: All round, furry things are quiet.
foreach
    round(?x, True),
    furry(?x, True)
assert
    quiet(?x, True).

# Rule: If Bob is blue and Bob is round then Bob is young.
foreach
    blue(Bob, True),
    round(Bob, True)
assert
    young(Bob, True).

# Rule: If something is round then it is blue.
foreach
    round(?x, True)
assert
    blue(?x, True).

# Rule: If something is young and round then it is blue.
foreach
    young(?x, True),
    round(?x, True)
assert
    blue(?x, True).

# Rule: If Harry is quiet and Harry is furry then Harry is blue.
foreach
    quiet(Harry, True),
    furry(Harry, True)
assert
    blue(Harry, True).

# Rule: Furry things are cold.
foreach
    furry(?x, True)
assert
    cold(?x, True).

# Rule: Cold things are round.
foreach
    cold(?x, True)
assert
    round(?x, True).

# Rule: If something is young and furry then it is rough.
foreach
    young(?x, True),
    furry(?x, True)
assert
    rough(?x, True).

query:
furry(Harry, True).