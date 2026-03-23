from pyke import knowledge_engine, goal

# Initialize knowledge engine
engine = knowledge_engine.engine(__file__)

# Add facts
engine.add_casebase('facts', None, [
    ('is_a', 'Max', 'numpus', True),
])

# Add rules
engine.add_rule('rompus_is_not_large', [
    ('is_a', '$thing', 'rompus', True)
], [
    ('is_large', '$thing', False)
])

engine.add_rule('rompus_is_numpus', [
    ('is_a', '$thing', 'rompus', True)
], [
    ('is_a', '$thing', 'numpus', True)
])

engine.add_rule('numpus_is_fruity', [
    ('is_a', '$thing', 'numpus', True)
], [
    ('is_fruity', '$thing', True)
])

engine.add_rule('numpus_is_wumpus', [
    ('is_a', '$thing', 'numpus', True)
], [
    ('is_a', '$thing', 'wumpus', True)
])

engine.add_rule('wumpus_is_not_metallic', [
    ('is_a', '$thing', 'wumpus', True)
], [
    ('is_metallic', '$thing', False)
])

engine.add_rule('wumpus_is_tumpus', [
    ('is_a', '$thing', 'wumpus', True)
], [
    ('is_a', '$thing', 'tumpus', True)
])

engine.add_rule('tumpus_is_cold', [
    ('is_a', '$thing', 'tumpus', True)
], [
    ('is_cold', '$thing', True)
])

engine.add_rule('dumpus_is_not_brown', [
    ('is_a', '$thing', 'dumpus', True)
], [
    ('is_brown', '$thing', False)
])

engine.add_rule('tumpus_is_jompus', [
    ('is_a', '$thing', 'tumpus', True)
], [
    ('is_a', '$thing', 'jompus', True)
])

engine.add_rule('jompus_is_sweet', [
    ('is_a', '$thing', 'jompus', True)
], [
    ('is_sweet', '$thing', True)
])

engine.add_rule('jompus_is_zumpus', [
    ('is_a', '$thing', 'jompus', True)
], [
    ('is_a', '$thing', 'zumpus', True)
])

engine.add_rule('zumpus_is_brown', [
    ('is_a', '$thing', 'zumpus', True)
], [
    ('is_brown', '$thing', True)
])

engine.add_rule('zumpus_is_yumpus', [
    ('is_a', '$thing', 'zumpus', True)
], [
    ('is_a', '$thing', 'yumpus', True)
])

# Activate the knowledge base
engine.activate('facts')

# Query: Is Max not brown? (i.e., is_brown("Max", False))
try:
    result = engine.query('facts', 'is_brown', ['Max', False])
    print("False" if result else "True")
except:
    # If query fails, we need to check if Max is brown through inference
    engine.reset()
    engine.activate('facts')
    
    # Try to prove Max is brown
    try:
        result_brown = engine.query('facts', 'is_brown', ['Max', True])
        if result_brown:
            print("False")  # Max is brown, so "Max is not brown" is false
        else:
            print("True")   # Max is not brown (or cannot be proven brown)
    except:
        print("True")  # Default if we can't prove it's brown