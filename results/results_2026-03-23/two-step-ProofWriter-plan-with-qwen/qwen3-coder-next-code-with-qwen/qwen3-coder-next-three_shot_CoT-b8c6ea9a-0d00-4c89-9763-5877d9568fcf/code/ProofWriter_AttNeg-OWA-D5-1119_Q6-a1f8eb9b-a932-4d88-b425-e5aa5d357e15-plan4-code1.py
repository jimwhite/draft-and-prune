# Import required PyKe modules
from pyke import knowledge_engine

# Create knowledge base
engine = knowledge_engine.engine(__file__)

# --- Facts ---
Facts:
is_blue, Anne, True
is_cold, Anne, True
is_kind, Anne, True
is_quiet, Anne, True

is_blue, Bob, True
is_kind, Bob, True
is_nice, Bob, True
is_quiet, Bob, False

is_furry, Dave, False
is_green, Dave, True
is_quiet, Dave, True

is_cold, Fiona, True

# --- Rules ---
Rules:
foreach is_cold($person, True)
    assert is_blue($person, True)

foreach is_green($person, True), is_nice($person, True)
    assert is_kind($person, True)

foreach is_blue($person, True)
    assert is_kind($person, True)

foreach is_kind($person, True), is_cold($person, True)
    assert is_nice($person, True)

foreach is_nice($person, True)
    assert is_green($person, True)

foreach is_cold($person, True), is_green($person, True)
    assert is_quiet($person, True)

# --- Query ---
Query:
facts.is_kind(Fiona, True)