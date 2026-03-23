# Import required modules (if needed for execution context)
from pyke import knowledge_engine

# --- Facts about individuals ---
is_cold("Bob", True)
is_quiet("Bob", True)
is_red("Bob", True)
is_smart("Bob", True)

# --- Facts about Charlie ---
is_kind("Charlie", True)
is_quiet("Charlie", True)
is_red("Charlie", True)
is_rough("Charlie", True)

# --- Facts about Dave ---
is_cold("Dave", True)
is_kind("Dave", True)
is_smart("Dave", True)

# --- Facts about Fiona ---
is_quiet("Fiona", True)

# --- Rules ---

# Rule: If something is quiet and cold then it is smart.
quiet_and_cold_is_smart
    foreach
        facts.is_quiet($thing, True)
        facts.is_cold($thing, True)
    assert
        facts.is_smart($thing, True)

# Rule: Red, cold things are round.
red_and_cold_is_round
    foreach
        facts.is_red($thing, True)
        facts.is_cold($thing, True)
    assert
        facts.is_round($thing, True)

# Rule: If something is kind and rough then it is red.
kind_and_rough_is_red
    foreach
        facts.is_kind($thing, True)
        facts.is_rough($thing, True)
    assert
        facts.is_red($thing, True)

# Rule: All quiet things are rough.
quiet_are_rough
    foreach
        facts.is_quiet($thing, True)
    assert
        facts.is_rough($thing, True)

# Rule: If something is cold and smart then it is red.
cold_and_smart_is_red
    foreach
        facts.is_cold($thing, True)
        facts.is_smart($thing, True)
    assert
        facts.is_red($thing, True)

# Rule: If something is rough then it is cold.
rough_is_cold
    foreach
        facts.is_rough($thing, True)
    assert
        facts.is_cold($thing, True)

# Rule: All red things are rough.
red_are_rough
    foreach
        facts.is_red($thing, True)
    assert
        facts.is_rough($thing, True)

# Rule: If Dave is smart and Dave is kind then Dave is quiet.
dave_smart_and_kind_is_quiet
    foreach
        facts.is_smart("Dave", True)
        facts.is_kind("Dave", True)
    assert
        facts.is_quiet("Dave", True)

# --- Query ---
facts.is_kind("Charlie", True)