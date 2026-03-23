from pyke import knowledge_engine

engine = knowledge_engine.engine(__file__)

# Facts
engine.add_predicate("is_blue", "bald_eagle", True)
engine.add_predicate("is_red", "bald_eagle", True)
engine.add_predicate("likes", "bald_eagle", "lion", True)
engine.add_predicate("needs", "bald_eagle", "bear", True)
engine.add_predicate("needs", "bald_eagle", "dog", True)
engine.add_predicate("is_blue", "bear", False)
engine.add_predicate("is_nice", "bear", True)
engine.add_predicate("needs", "bear", "dog", True)
engine.add_predicate("chases", "dog", "bald_eagle", True)
engine.add_predicate("is_red", "dog", True)
engine.add_predicate("needs", "dog", "bear", False)
engine.add_predicate("likes", "lion", "bear", False)

# Rules
@engine.rule
def rule1(x):
    if engine.query("likes", x, "lion", True) and \
       not engine.query("is_red", x, True):
        return ("chases", x, "lion", True)

@engine.rule
def rule2(x):
    if engine.query("is_red", x, True) and \
       engine.query("needs", x, "bald_eagle", True):
        return ("needs", "bald_eagle", "lion", True)

@engine.rule
def rule3(x):
    if engine.query("round", x, True):
        return ("likes", x, "dog", False)

@engine.rule
def rule4():
    if engine.query("needs", "bald_eagle", "dog", True):
        return ("round", "dog", True)

@engine.rule
def rule5(x):
    if engine.query("likes", x, "dog", True):
        return ("likes", x, "bald_eagle", True)

@engine.rule
def rule6(x):
    if engine.query("chases", x, "lion", True) and \
       engine.query("likes", "lion", "dog", True):
        return ("likes", "dog", "lion", False)

@engine.rule
def rule7():
    if engine.query("likes", "bear", "lion", True):
        return ("likes", "lion", "dog", True)

@engine.rule
def rule8(x):
    if engine.query("likes", x, "bear", True):
        return ("likes", "bear", "lion", True)

@engine.rule
def rule9(x):
    if engine.query("round", x, True):
        return ("likes", x, "bear", True)

# Query
engine.query("needs", "dog", "dog", False)