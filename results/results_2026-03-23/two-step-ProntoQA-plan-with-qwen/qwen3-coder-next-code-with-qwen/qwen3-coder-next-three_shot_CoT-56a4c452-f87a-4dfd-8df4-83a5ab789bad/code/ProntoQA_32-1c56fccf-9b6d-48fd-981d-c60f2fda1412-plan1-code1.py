from pyke import knowledge_engine

engine = knowledge_engine.engine(__file__)

# Facts section
engine.add_case_specific_fact(('facts', 'is_a'), ('Sally', 'numpus', True))
engine.add_case_specific_fact(('facts', 'is_a'), ('numpus', 'vumpus', True))
engine.add_case_specific_fact(('facts', 'is_a'), ('vumpus', 'tumpus', True))
engine.add_case_specific_fact(('facts', 'is_a'), ('tumpus', 'dumpus', True))
engine.add_case_specific_fact(('facts', 'is_a'), ('dumpus', 'wumpus', True))
engine.add_case_specific_fact(('facts', 'is_a'), ('wumpus', 'jompus', True))
engine.add_case_specific_fact(('facts', 'is_a'), ('jompus', 'zumpus', True))
engine.add_case_specific_fact(('facts', 'is_a'), ('zumpus', 'impus', True))
engine.add_case_specific_fact(('facts', 'is_a'), ('impus', 'yumpus', True))

# Properties
engine.add_case_specific_fact(('facts', 'is_earthy'), ('numpus', True))
engine.add_case_specific_fact(('facts', 'is_transparent'), ('vumpus', True))
engine.add_case_specific_fact(('facts', 'is_small'), ('tumpus', True))
engine.add_case_specific_fact(('facts', 'is_aggressive'), ('dumpus', False))
engine.add_case_specific_fact(('facts', 'is_wooden'), ('wumpus', False))
engine.add_case_specific_fact(('facts', 'is_nervous'), ('jompus', False))
engine.add_case_specific_fact(('facts', 'is_temperate'), ('zumpus', True))
engine.add_case_specific_fact(('facts', 'is_wooden'), ('rompus', True))
engine.add_case_specific_fact(('facts', 'is_blue'), ('impus', True))

# Rules section
engine.add_rule(
    ('rules', 'propagate_is_a'),
    """
    foreach facts.is_a($X, $Y, True)
              facts.is_earthy($Y, $Value)
    assert facts.is_earthy($X, $Value)
    
    foreach facts.is_a($X, $Y, True)
              facts.is_transparent($Y, $Value)
    assert facts.is_transparent($X, $Value)
    
    foreach facts.is_a($X, $Y, True)
              facts.is_small($Y, $Value)
    assert facts.is_small($X, $Value)
    
    foreach facts.is_a($X, $Y, True)
              facts.is_aggressive($Y, $Value)
    assert facts.is_aggressive($X, $Value)
    
    foreach facts.is_a($X, $Y, True)
              facts.is_wooden($Y, $Value)
    assert facts.is_wooden($X, $Value)
    
    foreach facts.is_a($X, $Y, True)
              facts.is_nervous($Y, $Value)
    assert facts.is_nervous($X, $Value)
    
    foreach facts.is_a($X, $Y, True)
              facts.is_temperate($Y, $Value)
    assert facts.is_temperate($X, $Value)
    
    foreach facts.is_a($X, $Y, True)
              facts.is_blue($Y, $Value)
    assert facts.is_blue($X, $Value)
    """
)

engine.activate('rules')

# Query section
result = engine.prove_1_goal(('facts', 'is_wooden', ('Sally', False)))
print(result is not None)