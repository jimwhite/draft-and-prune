# Import required modules
from pyke import knowledge_engine

# Create knowledge engine instance
engine = knowledge_engine.engine(__file__)

# --- Facts Section ---
Facts:
    is_big(Dave, True)
    is_furry(Dave, True)
    is_blue(Erin, True)
    is_cold(Erin, True)
    is_round(Erin, True)
    is_quiet(Fiona, True)
    is_rough(Gary, True)

# --- Rules Section ---
Rules:
    # If something is rough and cold then it is furry.
    foreach facts.is_rough($x, True)
              facts.is_cold($x, True)
        assert facts.is_furry($x, True)

    # Quiet, big things are not round.
    foreach facts.is_quiet($x, True)
              facts.is_big($x, True)
        assert facts.is_round($x, False)

    # If Dave is blue then Dave is furry.
    foreach facts.is_blue(Dave, True)
        assert facts.is_furry(Dave, True)

    # All quiet, blue things are big.
    foreach facts.is_quiet($x, True)
              facts.is_blue($x, True)
        assert facts.is_big($x, True)

    # If Fiona is furry then Fiona is blue.
    foreach facts.is_furry(Fiona, True)
        assert facts.is_blue(Fiona, True)

    # If something is quiet then it is cold.
    foreach facts.is_quiet($x, True)
        assert facts.is_cold($x, True)

    # All big things are cold.
    foreach facts.is_big($x, True)
        assert facts.is_cold($x, True)

    # All blue, round things are not quiet.
    foreach facts.is_blue($x, True)
              facts.is_round($x, True)
        assert facts.is_quiet($x, False)

    # Cold things are rough.
    foreach facts.is_cold($x, True)
        assert facts.is_rough($x, True)

# --- Query Section ---
Query:
    facts.is_furry(Erin, True)