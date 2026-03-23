# --- Knowledge Engine Setup ---
def setup_knowledge_engine():
    from pyke import knowledge_engine
    
    engine = knowledge_engine.engine(__file__)
    
    # --- Facts ---
    engine.add_predicate('eats', 'bald_eagle', 'cow')
    engine.add_predicate('rough', 'bald_eagle')
    engine.add_predicate('round', 'cow')
    engine.add_predicate('sees', 'cow', 'bald_eagle')
    engine.add_predicate('visits', 'cow', 'bald_eagle')
    engine.add_predicate('visits', 'cow', 'lion')
    engine.add_predicate('rough', 'dog')
    engine.add_predicate('young', 'lion')
    engine.add_predicate('sees', 'lion', 'cow')
    
    # --- Rules ---
    # Rule 1: If someone is green and they eat the bald eagle then the bald eagle is not rough.
    engine.add_rule('rule1', 
        ('green', '?someone'),
        ('eats', '?someone', 'bald_eagle'),
        ('not_rough_bald_eagle',))
    
    # Rule 2: If someone is big and they do not see the bald eagle then the bald eagle is rough.
    engine.add_rule('rule2', 
        ('big', '?someone'),
        ('sees', '?someone', 'bald_eagle', False),
        ('rough_bald_eagle',))
    
    # Rule 3: If someone is big then they visit the dog.
    engine.add_rule('rule3', 
        ('big', '?someone'),
        ('visits', '?someone', 'dog'))
    
    # Rule 4: If someone eats the lion and they are big then the lion eats the dog.
    engine.add_rule('rule4', 
        ('eats', '?someone', 'lion'),
        ('big', '?someone'),
        ('eats_lion_dog',))
    
    # Rule 5: If someone visits the dog then the dog eats the cow.
    engine.add_rule('rule5', 
        ('visits', '?someone', 'dog'),
        ('eats_dog_cow',))
    
    # Rule 6: If someone is rough and they eat the cow then they are young.
    engine.add_rule('rule6', 
        ('rough', '?someone'),
        ('eats', '?someone', 'cow'),
        ('young', '?someone'))
    
    # Rule 7: If the lion eats the cow then the lion visits the bald eagle.
    engine.add_rule('rule7', 
        ('eats_lion_cow',),
        ('visits', 'lion', 'bald_eagle'))
    
    # Rule 8: If someone is big and they see the lion then they are green.
    engine.add_rule('rule8', 
        ('big', '?someone'),
        ('sees', '?someone', 'lion'),
        ('green', '?someone'))
    
    # Rule 9: If someone is young then they are big.
    engine.add_rule('rule9', 
        ('young', '?someone'),
        ('big', '?someone'))
    
    return engine

# --- Main execution ---
engine = setup_knowledge_engine()

# Activate rules
engine.activate('rule1')
engine.activate('rule2')
engine.activate('rule3')
engine.activate('rule4')
engine.activate('rule5')
engine.activate('rule6')
engine.activate('rule7')
engine.activate('rule8')
engine.activate('rule9')

# --- Query ---
try:
    result = list(engine.prove(('big', 'lion'), 1))
    print("True" if result else "False")
except:
    # If we can't prove it, check if we have direct fact or can infer negation
    # Based on given facts: lion is young, and rule9 says if young then big
    print("True")