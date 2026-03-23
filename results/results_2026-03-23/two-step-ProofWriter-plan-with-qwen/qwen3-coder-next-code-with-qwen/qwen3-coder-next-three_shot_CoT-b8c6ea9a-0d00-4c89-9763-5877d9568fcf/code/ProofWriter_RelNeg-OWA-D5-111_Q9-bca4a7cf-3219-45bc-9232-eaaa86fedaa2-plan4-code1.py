from pyke import knowledge_engine

# Initialize the knowledge engine
engine = knowledge_engine.engine(__file__)

# --- Facts ---
engine.add_case_fact('facts', ('chases', 'bald_eagle', 'mouse'))
engine.add_case_fact('facts', ('chases', 'bald_eagle', 'squirrel'))
engine.add_case_fact('facts', ('is_cold', 'bald_eagle'))

engine.add_case_fact('facts', ('chases', 'lion', 'bald_eagle'))
engine.add_case_fact('facts', ('chases', 'lion', 'squirrel'))
engine.add_case_fact('facts', ('is_blue', 'lion'))
engine.add_case_fact('facts', ('needs', 'lion', 'squirrel'))
engine.add_case_fact('facts', ('visits', 'lion', 'squirrel'))

# Mouse does not chase lion (so we add negative fact)
engine.add_case_fact('facts', ('chases', 'mouse', 'lion'), False)

# Mouse does not visit bald eagle or squirrel
engine.add_case_fact('facts', ('visits', 'mouse', 'bald_eagle'), False)
engine.add_case_fact('facts', ('visits', 'mouse', 'squirrel'), False)

# Squirrel properties
engine.add_case_fact('facts', ('is_cold', 'squirrel'))
engine.add_case_fact('facts', ('is_red', 'squirrel'))
engine.add_case_fact('facts', ('visits', 'squirrel', 'lion'), False)

# --- Rules ---
engine.add_rule('rules', 
    # If something visits the mouse then the mouse is green.
    ('(?x, "mouse")', 'visits'),
    ('is_green', 'mouse'))

engine.add_rule('rules',
    # If the mouse does not chase the lion then the mouse needs the lion.
    ('("mouse", "lion")', 'chases', False),
    ('needs', 'mouse', 'lion'))

engine.add_rule('rules',
    # If something visits the squirrel and the squirrel does not chase the lion then the lion is green.
    ('(?x, "squirrel")', 'visits'),
    ('("squirrel", "lion")', 'chases', False),
    ('is_green', 'lion'))

engine.add_rule('rules',
    # If something is young then it visits the bald eagle.
    ('(?x)', 'is_young'),
    ('visits', '?x', 'bald_eagle'))

engine.add_rule('rules',
    # If something visits the bald eagle then the bald eagle visits the squirrel.
    ('(?x, "bald_eagle")', 'visits'),
    ('visits', 'bald_eagle', 'squirrel'))

engine.add_rule('rules',
    # If something visits the squirrel and the squirrel is red then it is young.
    ('(?x, "squirrel")', 'visits'),
    ('"squirrel"', 'is_red'),
    ('is_young', '?x'))

engine.add_rule('rules',
    # If something needs the squirrel and it is not cold then the squirrel chases the bald eagle.
    ('(?x, "squirrel")', 'needs'),
    ('?x', 'is_cold', False),
    ('chases', 'squirrel', 'bald_eagle'))

# --- Query ---
engine.add_query('facts', ('is_young', 'bald_eagle'))