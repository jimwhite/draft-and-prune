# Facts about entities
Facts:
    is_furry(Anne, True)
    is_furry(Bob, True)
    is_blue(Gary, True)
    is_cold(Gary, True)
    is_furry(Gary, True)
    is_quiet(Gary, True)
    is_round(Gary, True)
    is_blue(Harry, True)
    is_cold(Harry, True)
    is_quiet(Harry, True)
    is_round(Harry, True)
    is_young(Harry, True)

# Rules for inference
Rules:
    # Rule: Cold and blue things are quiet.
    foreach facts.is_cold($thing, True)
            facts.is_blue($thing, True)
        assert facts.is_quiet($thing, True)

    # Rule: All round, furry things are quiet.
    foreach facts.is_round($thing, True)
            facts.is_furry($thing, True)
        assert facts.is_quiet($thing, True)

    # Rule: If Bob is blue and Bob is round then Bob is young.
    foreach facts.is_blue(Bob, True)
            facts.is_round(Bob, True)
        assert facts.is_young(Bob, True)

    # Rule: If something is round then it is blue.
    foreach facts.is_round($thing, True)
        assert facts.is_blue($thing, True)

    # Rule: If something is young and round then it is blue.
    foreach facts.is_young($thing, True)
            facts.is_round($thing, True)
        assert facts.is_blue($thing, True)

    # Rule: If Harry is quiet and Harry is furry then Harry is blue.
    foreach facts.is_quiet(Harry, True)
            facts.is_furry(Harry, True)
        assert facts.is_blue(Harry, True)

    # Rule: Furry things are cold.
    foreach facts.is_furry($thing, True)
        assert facts.is_cold($thing, True)

    # Rule: Cold things are round.
    foreach facts.is_cold($thing, True)
        assert facts.is_round($thing, True)

    # Rule: If something is young and furry then it is rough.
    foreach facts.is_young($thing, True)
            facts.is_furry($thing, True)
        assert facts.is_rough($thing, True)

# Query: Is Harry furry?
Query:
    facts.is_furry(Harry, True)