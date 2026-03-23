# --- Facts ---
def is_big(x):
    return x == "Charlie"

def is_cold(x):
    return x == "Charlie"

def is_kind(x):
    return x in ["Charlie", "Erin", "Harry"]

def is_quiet(x):
    return x in ["Charlie", "Fiona"]

def is_red(x):
    return x == "Charlie"

def is_rough(x):
    return x in ["Charlie", "Fiona", "Harry"]

def is_smart(x):
    return x == "Charlie"

# --- Rules ---
from pyke import knowledge_engine

engine = knowledge_engine.engine(__file__)

@engine.rule
def kind_implies_big():
    """
    Kind things are big.
    """
    return [
        (is_kind(x), is_big(x))
        for x in ["Charlie", "Erin", "Harry"]
    ]

@engine.rule
def kind_and_smart_implies_rough():
    """
    All kind, smart things are rough.
    """
    return [
        (is_kind(x) and is_smart(x), is_rough(x))
        for x in ["Charlie", "Erin", "Harry"]
    ]

@engine.rule
def red_and_quiet_implies_big():
    """
    If something is red and quiet then it is big.
    """
    return [
        (is_red(x) and is_quiet(x), is_big(x))
        for x in ["Charlie", "Fiona"]
    ]

@engine.rule
def red_implies_cold():
    """
    All red things are cold.
    """
    return [
        (is_red(x), is_cold(x))
        for x in ["Charlie"]
    ]

@engine.rule
def cold_and_quiet_implies_smart():
    """
    All cold, quiet things are smart.
    """
    return [
        (is_cold(x) and is_quiet(x), is_smart(x))
        for x in ["Charlie", "Fiona"]
    ]

@engine.rule
def big_and_smart_implies_cold():
    """
    If something is big and smart then it is cold.
    """
    return [
        (is_big(x) and is_smart(x), is_cold(x))
        for x in ["Charlie"]
    ]

@engine.rule
def quiet_implies_cold():
    """
    All quiet things are cold.
    """
    return [
        (is_quiet(x), is_cold(x))
        for x in ["Charlie", "Fiona"]
    ]

@engine.rule
def kind_and_big_implies_red():
    """
    Kind, big things are red.
    """
    return [
        (is_kind(x) and is_big(x), is_red(x))
        for x in ["Charlie", "Erin", "Harry"]
    ]

@engine.rule
def cold_and_smart_implies_kind():
    """
    All cold, smart things are kind.
    """
    return [
        (is_cold(x) and is_smart(x), is_kind(x))
        for x in ["Charlie", "Fiona"]
    ]

# --- Query ---
def query_fiona_not_red():
    """
    Is Fiona not red?
    """
    return not is_red("Fiona")