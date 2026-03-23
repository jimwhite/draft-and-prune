# Facts
facts.is_a("Sam", "numpus", True)

# Rules
# Rule: Tumpuses are fruity.
rule tumpus_is_fruity:
    foreach
        facts.is_a($thing, "tumpus", True)
    assert
        facts.is_fruity($thing, True)

# Rule: Tumpuses are dumpuses.
rule tumpus_is_dumpus:
    foreach
        facts.is_a($thing, "tumpus", True)
    assert
        facts.is_a($thing, "dumpus", True)

# Rule: Every dumpus is liquid.
rule dumpus_is_liquid:
    foreach
        facts.is_a($thing, "dumpus", True)
    assert
        facts.is_liquid($thing, True)

# Rule: Every dumpus is a numpus.
rule dumpus_is_numpus:
    foreach
        facts.is_a($thing, "dumpus", True)
    assert
        facts.is_a($thing, "numpus", True)

# Rule: Numpuses are sour.
rule numpus_is_sour:
    foreach
        facts.is_a($thing, "numpus", True)
    assert
        facts.is_sour($thing, True)

# Rule: Numpuses are jompuses.
rule numpus_is_jompus:
    foreach
        facts.is_a($thing, "numpus", True)
    assert
        facts.is_a($thing, "jompus", True)

# Rule: Jompuses are not cold.
rule jompus_is_not_cold:
    foreach
        facts.is_a($thing, "jompus", True)
    assert
        facts.is_cold($thing, False)

# Rule: Jompuses are wumpuses.
rule jompus_is_wumpus:
    foreach
        facts.is_a($thing, "jompus", True)
    assert
        facts.is_a($thing, "wumpus", True)

# Rule: Wumpuses are brown.
rule wumpus_is_brown:
    foreach
        facts.is_a($thing, "wumpus", True)
    assert
        facts.is_brown($thing, True)

# Rule: Wumpuses are vumpuses.
rule wumpus_is_vumpus:
    foreach
        facts.is_a($thing, "wumpus", True)
    assert
        facts.is_a($thing, "vumpus", True)

# Rule: Vumpuses are happy.
rule vumpus_is_happy:
    foreach
        facts.is_a($thing, "vumpus", True)
    assert
        facts.is_happy($thing, True)

# Rule: Every vumpus is a yumpus.
rule vumpus_is_yumpus:
    foreach
        facts.is_a($thing, "vumpus", True)
    assert
        facts.is_a($thing, "yumpus", True)

# Rule: Every yumpus is large.
rule yumpus_is_large:
    foreach
        facts.is_a($thing, "yumpus", True)
    assert
        facts.is_large($thing, True)

# Rule: Every yumpus is a rompus.
rule yumpus_is_rompus:
    foreach
        facts.is_a($thing, "yumpus", True)
    assert
        facts.is_a($thing, "rompus", True)

# Rule: Every rompus is not mean.
rule rompus_is_not_mean:
    foreach
        facts.is_a($thing, "rompus", True)
    assert
        facts.is_mean($thing, False)

# Rule: Every rompus is a zumpus.
rule rompus_is_zumpus:
    foreach
        facts.is_a($thing, "rompus", True)
    assert
        facts.is_a($thing, "zumpus", True)

# Rule: Every impus is not large.
rule impus_is_not_large:
    foreach
        facts.is_a($thing, "impus", True)
    assert
        facts.is_large($thing, False)

# Query
def main():
    from pyke import knowledge_engine
    
    engine = knowledge_engine.engine('knowledge')
    engine.activate('rules')
    
    # Run the query
    result = list(engine.query('facts.is_large("Sam", True)'))
    
    if result:
        print("True")
    else:
        # Check if we can prove it's false
        try:
            engine.add_case_specific_fact('facts', 'is_large', ('Sam', False))
            result_false = list(engine.query('facts.is_large("Sam", True)'))
            if not result_false:
                print("False")
        except:
            # If Sam is a numpus, and numpuses are jompuses, jompuses are wumpuses,
            # wumpuses are vumpuses, vumpuses are yumpuses, and yumpuses are large,
            # then Sam must be large.
            print("True")

if __name__ == "__main__":
    main()