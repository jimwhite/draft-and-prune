# Facts about entities
Facts:
is_furry Anne True
is_furry Bob True
is_blue Gary True
is_cold Gary True
is_furry Gary True
is_quiet Gary True
is_round Gary True
is_blue Harry True
is_cold Harry True
is_quiet Harry True
is_round Harry True
is_young Harry True

# Rules for inference
Rules:
# Cold, blue things are quiet.
foreach
    ?thing is_cold ?thing True
    ?thing is_blue ?thing True
assert
    ?thing is_quiet ?thing True

# All round, furry things are quiet.
foreach
    ?thing is_round ?thing True
    ?thing is_furry ?thing True
assert
    ?thing is_quiet ?thing True

# If Bob is blue and Bob is round then Bob is young.
foreach
    Bob is_blue Bob True
    Bob is_round Bob True
assert
    Bob is_young Bob True

# If something is round then it is blue.
foreach
    ?thing is_round ?thing True
assert
    ?thing is_blue ?thing True

# If something is young and round then it is blue.
foreach
    ?thing is_young ?thing True
    ?thing is_round ?thing True
assert
    ?thing is_blue ?thing True

# If Harry is quiet and Harry is furry then Harry is blue.
foreach
    Harry is_quiet Harry True
    Harry is_furry Harry True
assert
    Harry is_blue Harry True

# Furry things are cold.
foreach
    ?thing is_furry ?thing True
assert
    ?thing is_cold ?thing True

# Cold things are round.
foreach
    ?thing is_cold ?thing True
assert
    ?thing is_round ?thing True

# If something is young and furry then it is rough.
foreach
    ?thing is_young ?thing True
    ?thing is_furry ?thing True
assert
    ?thing is_rough ?thing True

# Query: Is Harry furry?
Query:
is_furry Harry True