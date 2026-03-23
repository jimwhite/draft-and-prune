import pyke

# Initialize knowledge engine
knowledge_engine = pyke.engine()

# Facts
facts = [
    ("eats", "cat", "squirrel"),
    ("sees", "cat", "squirrel"),
    ("eats", "cow", "squirrel"),
    ("sees", "cow", "cat"),
    ("is_round", "rabbit"),
    ("sees", "rabbit", "cat"),
    ("eats", "squirrel", "rabbit"),
    ("is_cold", "squirrel"),
    ("needs", "squirrel", "rabbit"),
    ("sees", "squirrel", "cat")
]

# Rules
rules = [
    # If someone sees the cat and they are not green then they see the cow
    ("sees(X, 'cat')", "not is_green(X)", "sees(X, 'cow')"),
    
    # Rough people are cold
    ("is_rough(X)", "is_cold(X)"),
    
    # If someone sees the rabbit then they are not round
    ("sees(X, 'rabbit')", "not is_round(X)"),
    
    # If someone sees the squirrel and they are not green then they need the squirrel
    ("sees(X, 'squirrel')", "not is_green(X)", "needs(X, 'squirrel')"),
    
    # If someone eats the cow then they see the rabbit
    ("eats(X, 'cow')", "sees(X, 'rabbit')"),
    
    # If someone eats the squirrel then they are rough
    ("eats(X, 'squirrel')", "is_rough(X)"),
    
    # If someone is cold then they eat the cow
    ("is_cold(X)", "eats(X, 'cow')")
]

# Add facts to knowledge base
for fact in facts:
    if len(fact) == 3 and fact[0] in ['eats', 'sees', 'needs']:
        knowledge_engine.add_fact(fact[0], fact[1], fact[2])
    elif len(fact) == 2 and fact[0] in ['is_round', 'is_cold', 'is_green', 'is_rough', 'is_kind']:
        knowledge_engine.add_fact(fact[0], fact[1])

# Add rules to knowledge base
for rule in rules:
    if len(rule) == 3:  # binary rule with two conditions
        knowledge_engine.add_rule(rule[0], rule[1], rule[2])
    elif len(rule) == 2:  # unary rule
        knowledge_engine.add_rule(rule[0], rule[1])

# Query: is the cat not round?
query = ("is_round", "cat")
result = knowledge_engine.query(query)

# Since we want to check if cat is NOT round, we need to see if is_round("cat") fails
# If the query returns False (or no proof), then "cat is not round" is True
# If the query returns True, then "cat is not round" is False

if result:
    print("False")  # cat IS round, so "cat is not round" is false
else:
    print("True")   # cat is NOT round (unknown or proven false), so statement is true