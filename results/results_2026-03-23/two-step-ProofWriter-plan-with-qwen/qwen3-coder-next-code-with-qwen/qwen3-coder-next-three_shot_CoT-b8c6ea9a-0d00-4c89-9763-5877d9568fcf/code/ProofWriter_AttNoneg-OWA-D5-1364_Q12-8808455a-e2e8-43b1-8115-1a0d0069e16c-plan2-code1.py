from pyke import knowledge_engine

# Create knowledge engine instance
engine = knowledge_engine.engine(__file__)

# --- Facts ---
def is_big(subject, value):
    return value

def is_cold(subject, value):
    return value

def is_kind(subject, value):
    return value

def is_quiet(subject, value):
    return value

def is_red(subject, value):
    return value

def is_rough(subject, value):
    return value

def is_smart(subject, value):
    return value

# Explicit facts
is_big("Charlie", True)
is_cold("Charlie", True)
is_kind("Charlie", True)
is_quiet("Charlie", True)
is_red("Charlie", True)
is_rough("Charlie", True)
is_smart("Charlie", True)

is_kind("Erin", True)

is_quiet("Fiona", True)
is_rough("Fiona", True)

is_kind("Harry", True)
is_rough("Harry", True)

# --- Rules ---
@engine.rule
def kind_implies_big(?x):
    return is_kind(?x, True), is_big(?x, True)

@engine.rule
def kind_and_smart_implies_rough(?x):
    return is_kind(?x, True), is_smart(?x, True), is_rough(?x, True)

@engine.rule
def red_and_quiet_implies_big(?x):
    return is_red(?x, True), is_quiet(?x, True), is_big(?x, True)

@engine.rule
def red_implies_cold(?x):
    return is_red(?x, True), is_cold(?x, True)

@engine.rule
def cold_and_quiet_implies_smart(?x):
    return is_cold(?x, True), is_quiet(?x, True), is_smart(?x, True)

@engine.rule
def big_and_smart_implies_cold(?x):
    return is_big(?x, True), is_smart(?x, True), is_cold(?x, True)

@engine.rule
def quiet_implies_cold(?x):
    return is_quiet(?x, True), is_cold(?x, True)

@engine.rule
def kind_and_big_implies_red(?x):
    return is_kind(?x, True), is_big(?x, True), is_red(?x, True)

@engine.rule
def cold_and_smart_implies_kind(?x):
    return is_cold(?x, True), is_smart(?x, True), is_kind(?x, True)

# --- Query ---
def query_fiona_not_red():
    # We want to check if "Fiona is not red" is true
    # This means we need to prove that is_red("Fiona", True) is false
    return not is_red("Fiona", True)