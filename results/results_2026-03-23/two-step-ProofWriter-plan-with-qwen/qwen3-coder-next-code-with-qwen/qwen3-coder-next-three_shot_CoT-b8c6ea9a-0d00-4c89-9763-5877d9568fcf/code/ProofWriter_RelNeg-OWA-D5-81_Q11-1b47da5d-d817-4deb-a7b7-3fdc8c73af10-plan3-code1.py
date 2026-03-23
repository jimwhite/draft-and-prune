import pyke

# Initialize knowledge engine
knowledge_engine = pyke.engine()

# Facts
knowledge_engine.add_fact("eats", "cat", "squirrel")
knowledge_engine.add_fact("sees", "cat", "squirrel")
knowledge_engine.add_fact("eats", "cow", "squirrel")
knowledge_engine.add_fact("sees", "cow", "cat")
knowledge_engine.add_fact("is_round", "rabbit")
knowledge_engine.add_fact("sees", "rabbit", "cat")
knowledge_engine.add_fact("eats", "squirrel", "rabbit")
knowledge_engine.add_fact("is_cold", "squirrel")
knowledge_engine.add_fact("needs", "squirrel", "rabbit")
knowledge_engine.add_fact("sees", "squirrel", "cat")

# Rules
@knowledge_engine.rule
def sees_cat_not_green_sees_cow(X):
    if knowledge_engine.query("sees", X, "cat") and not knowledge_engine.query("is_green", X):
        return ("sees", X, "cow")

@knowledge_engine.rule
def is_rough_is_cold(X):
    if knowledge_engine.query("is_rough", X):
        return ("is_cold", X)

@knowledge_engine.rule
def sees_rabbit_not_round(X):
    if knowledge_engine.query("sees", X, "rabbit"):
        return ("not_round", X)

@knowledge_engine.rule
def sees_squirrel_not_green_needs_squirrel(X):
    if knowledge_engine.query("sees", X, "squirrel") and not knowledge_engine.query("is_green", X):
        return ("needs", X, "squirrel")

@knowledge_engine.rule
def eats_cow_sees_rabbit(X):
    if knowledge_engine.query("eats", X, "cow"):
        return ("sees", X, "rabbit")

@knowledge_engine.rule
def eats_squirrel_is_rough(X):
    if knowledge_engine.query("eats", X, "squirrel"):
        return ("is_rough", X)

@knowledge_engine.rule
def is_cold_eats_cow(X):
    if knowledge_engine.query("is_cold", X):
        return ("eats", X, "cow")

# Query: is the cat not round?
result = knowledge_engine.query("is_round", "cat")
# The statement is "The cat is not round" which means is_round("cat") should be False
# So we check if not is_round("cat")
is_cat_not_round = not result

print(is_cat_not_round)