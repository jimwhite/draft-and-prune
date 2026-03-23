from pyke import knowledge_engine

# Create knowledge engine instance
engine = knowledge_engine.engine(__file__)

# --- Facts ---
def add_facts():
    engine.add_case_fact('facts', ('chases', 'bald_eagle', 'mouse'))
    engine.add_case_fact('facts', ('chases', 'bald_eagle', 'squirrel'))
    engine.add_case_fact('facts', ('is_cold', 'bald_eagle'))

    engine.add_case_fact('facts', ('chases', 'lion', 'bald_eagle'))
    engine.add_case_fact('facts', ('chases', 'lion', 'squirrel'))
    engine.add_case_fact('facts', ('is_blue', 'lion'))
    engine.add_case_fact('facts', ('needs', 'lion', 'squirrel'))
    engine.add_case_fact('facts', ('visits', 'lion', 'squirrel'))

    engine.add_case_fact('facts', ('is_cold', 'squirrel'))
    engine.add_case_fact('facts', ('is_red', 'squirrel'))

# --- Rules ---
@engine.rule
def mouse_green_if_visited():
    """
    If something visits the mouse then the mouse is green.
    """
    yield from engine.query('facts', ('visits', '?x', 'mouse'))
    engine.add_case_fact('facts', ('is_green', 'mouse'))

@engine.rule
def mouse_needs_lion_if_not_chase():
    """
    If the mouse does not chase the lion then the mouse needs the lion.
    Note: We need to check that chases(mouse, lion) is NOT a fact
    """
    # Since we don't have explicit negative facts in PyKe, we check absence
    if not any(f for f in engine.knowledge_bases['facts'].get_case_facts() 
               if f[0] == 'chases' and f[1] == 'mouse' and f[2] == 'lion'):
        engine.add_case_fact('facts', ('needs', 'mouse', 'lion'))

@engine.rule
def lion_green_if_visits_squirrel_and_squirrel_not_chase_lion():
    """
    If something visits the squirrel and the squirrel does not chase the lion then the lion is green.
    """
    yield from engine.query('facts', ('visits', '?x', 'squirrel'))
    # Check that squirrel does not chase lion
    if not any(f for f in engine.knowledge_bases['facts'].get_case_facts() 
               if f[0] == 'chases' and f[1] == 'squirrel' and f[2] == 'lion'):
        engine.add_case_fact('facts', ('is_green', 'lion'))

@engine.rule
def young_visits_bald_eagle():
    """
    If something is young then it visits the bald eagle.
    """
    yield from engine.query('facts', ('is_young', '?x'))
    engine.add_case_fact('facts', ('visits', '?x', 'bald_eagle'))

@engine.rule
def visits_bald_eagle_then_visits_squirrel():
    """
    If something visits the bald eagle then the bald eagle visits the squirrel.
    """
    yield from engine.query('facts', ('visits', '?x', 'bald_eagle'))
    engine.add_case_fact('facts', ('visits', 'bald_eagle', 'squirrel'))

@engine.rule
def visits_squirrel_and_red_then_young():
    """
    If something visits the squirrel and the squirrel is red then it is young.
    """
    yield from engine.query('facts', ('visits', '?x', 'squirrel'))
    yield from engine.query('facts', ('is_red', 'squirrel'))
    engine.add_case_fact('facts', ('is_young', '?x'))

@engine.rule
def needs_squirrel_and_not_cold_then_squirrel_chases_bald_eagle():
    """
    If something needs the squirrel and it is not cold then the squirrel chases the bald eagle.
    """
    yield from engine.query('facts', ('needs', '?x', 'squirrel'))
    # Check that ?x is not cold
    if not any(f for f in engine.knowledge_bases['facts'].get_case_facts() 
               if f[0] == 'is_cold' and f[1] == '?x'):
        engine.add_case_fact('facts', ('chases', 'squirrel', 'bald_eagle'))

# --- Query ---
def main():
    # Initialize and add facts
    engine.reset()
    add_facts()
    
    # Run forward chaining to derive new facts
    engine.activate('rules')
    
    # Query: is the bald eagle young?
    try:
        result = list(engine.query('facts', ('is_young', 'bald_eagle')))
        if result:
            print("True")
        else:
            # Check if we can prove it's not young
            # In PyKe, absence of proof doesn't mean false, so we check derived facts
            print("Unknown")
    except:
        print("Unknown")

if __name__ == "__main__":
    main()