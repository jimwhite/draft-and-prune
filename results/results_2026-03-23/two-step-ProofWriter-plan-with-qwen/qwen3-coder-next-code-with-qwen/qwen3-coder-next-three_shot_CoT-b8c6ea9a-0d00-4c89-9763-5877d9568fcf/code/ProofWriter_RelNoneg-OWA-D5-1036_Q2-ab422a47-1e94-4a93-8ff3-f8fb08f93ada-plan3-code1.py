from pyke import knowledge_engine

engine = knowledge_engine.engine(__file__)

# Facts
engine.add_rule('facts', 'eats', ('bear', 'squirrel'), True)
engine.add_rule('facts', 'is_cold', ('bear',), True)
engine.add_rule('facts', 'is_rough', ('bear',), True)
engine.add_rule('facts', 'visits', ('bear', 'lion'), True)
engine.add_rule('facts', 'eats', ('cat', 'lion'), True)
engine.add_rule('facts', 'likes', ('lion', 'cat'), True)
engine.add_rule('facts', 'visits', ('lion', 'bear'), True)
engine.add_rule('facts', 'eats', ('squirrel', 'lion'), True)
engine.add_rule('facts', 'is_cold', ('squirrel',), True)
engine.add_rule('facts', 'is_rough', ('squirrel',), True)
engine.add_rule('facts', 'likes', ('squirrel', 'bear'), True)
engine.add_rule('facts', 'visits', ('squirrel', 'lion'), True)

# Rule: Red people are green (if someone is red, they are green)
engine.add_rule('rules', 'red_implies_green', 
    ('X',), 
    [('is_red', ('X',))], 
    [('is_green', ('X',))])

# Rule: If someone eats the lion then the lion is red
engine.add_rule('rules', 'eats_lion_makes_lion_red',
    (), 
    [('eats', ('X', 'lion'))], 
    [('is_red', ('lion',))])

# Rule: If someone is green and they like the lion then they eat the bear
engine.add_rule('rules', 'green_and_likes_lion_eats_bear',
    ('X',), 
    [('is_green', ('X',)), ('likes', ('X', 'lion'))], 
    [('eats', ('X', 'bear'))])

# Rule: If someone visits the bear then the bear likes the lion
engine.add_rule('rules', 'visits_bear_bear_likes_lion',
    (), 
    [('visits', ('X', 'bear'))], 
    [('likes', ('bear', 'lion'))])

# Rule: If someone likes the squirrel and they like the lion then they visit the lion
engine.add_rule('rules', 'likes_squirrel_and_lion_visits_lion',
    ('X',), 
    [('likes', ('X', 'squirrel')), ('likes', ('X', 'lion'))], 
    [('visits', ('X', 'lion'))])

# Rule: If someone is green then they eat the squirrel
engine.add_rule('rules', 'green_eats_squirrel',
    ('X',), 
    [('is_green', ('X',))], 
    [('eats', ('X', 'squirrel'))])

# Rule: If someone likes the lion then they visit the bear
engine.add_rule('rules', 'likes_lion_visits_bear',
    ('X',), 
    [('likes', ('X', 'lion'))], 
    [('visits', ('X', 'bear'))])

# Rule: If someone visits the lion and the lion is green then they are red
engine.add_rule('rules', 'visits_lion_and_lion_green_is_red',
    ('X',), 
    [('visits', ('X', 'lion')), ('is_green', ('lion',))], 
    [('is_red', ('X',))])

# Query: is the squirrel not rough?
engine.add_query('query', 'is_rough_squirrel_not_rough',
    [('is_rough', ('squirrel',))])

# Run the engine
engine.activate('rules')

# Check if we can prove squirrel is rough (should be True based on facts)
result = list(engine.prove('query', 'is_rough_squirrel_not_rough', 1))

# The query asks if squirrel is NOT rough, so we need to check the negation
if result:
    # If we can prove squirrel IS rough, then "squirrel is not rough" is FALSE
    print("False")
else:
    # If we cannot prove squirrel IS rough, then "squirrel is not rough" might be TRUE or UNKNOWN
    # But from the facts, we know "is_rough('squirrel', True)" is explicitly stated
    print("Unknown")