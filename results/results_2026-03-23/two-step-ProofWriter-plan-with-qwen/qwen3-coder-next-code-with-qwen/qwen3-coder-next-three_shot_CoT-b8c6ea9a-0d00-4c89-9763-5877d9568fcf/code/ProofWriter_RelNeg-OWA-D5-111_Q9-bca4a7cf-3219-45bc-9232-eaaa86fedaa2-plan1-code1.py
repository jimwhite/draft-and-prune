# --- Facts ---
def fact_chases_bald_eagle_mouse():
    return ("bald_eagle", "mouse")

def fact_chases_bald_eagle_squirrel():
    return ("bald_eagle", "squirrel")

def fact_is_cold_bald_eagle():
    return ("bald_eagle",)

def fact_chases_lion_bald_eagle():
    return ("lion", "bald_eagle")

def fact_chases_lion_squirrel():
    return ("lion", "squirrel")

def fact_is_blue_lion():
    return ("lion",)

def fact_needs_lion_squirrel():
    return ("lion", "squirrel")

def fact_visits_lion_squirrel():
    return ("lion", "squirrel")

def fact_is_cold_squirrel():
    return ("squirrel",)

def fact_is_red_squirrel():
    return ("squirrel",)

# --- Rules ---
@rule(
    "If something visits the mouse then the mouse is green.",
    lambda x: visits(x, "mouse")
)
def rule_mouse_green(x):
    return is_green("mouse")

@rule(
    "If the mouse does not chase the lion then the mouse needs the lion.",
    lambda: chases("mouse", "lion") == False
)
def rule_mouse_needs_lion():
    return needs("mouse", "lion")

@rule(
    "If something visits the squirrel and the squirrel does not chase the lion then the lion is green.",
    lambda x: visits(x, "squirrel") and chases("squirrel", "lion") == False
)
def rule_lion_green(x):
    return is_green("lion")

@rule(
    "If something is young then it visits the bald eagle.",
    lambda x: is_young(x)
)
def rule_young_visits_bald_eagle(x):
    return visits(x, "bald_eagle")

@rule(
    "If something visits the bald eagle then the bald eagle visits the squirrel.",
    lambda x: visits(x, "bald_eagle")
)
def rule_bald_eagle_visits_squirrel(x):
    return visits("bald_eagle", "squirrel")

@rule(
    "If something visits the squirrel and the squirrel is red then it is young.",
    lambda x: visits(x, "squirrel") and is_red("squirrel")
)
def rule_visits_squirrel_is_young(x):
    return is_young(x)

@rule(
    "If something needs the squirrel and it is not cold then the squirrel chases the bald eagle.",
    lambda x: needs(x, "squirrel") and is_cold(x) == False
)
def rule_squirrel_chases_bald_eagle(x):
    return chases("squirrel", "bald_eagle")

# --- Query ---
def query_is_young_bald_eagle():
    return is_young("bald_eagle")