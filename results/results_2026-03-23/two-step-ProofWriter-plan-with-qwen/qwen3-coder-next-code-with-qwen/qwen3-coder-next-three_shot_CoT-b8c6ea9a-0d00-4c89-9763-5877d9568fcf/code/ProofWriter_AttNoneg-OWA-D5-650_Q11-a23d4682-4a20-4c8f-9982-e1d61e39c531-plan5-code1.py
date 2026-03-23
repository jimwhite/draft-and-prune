from pyke import knowledge_engine

# Create knowledge engine instance
engine = knowledge_engine.engine(__file__)

# Define the knowledge base with proper PyKe syntax
engine.add_rule('facts',
    ('is_smart', 'Anne'),
    (),
    ())

engine.add_rule('facts',
    ('is_nice', 'Charlie'),
    (),
    ())

engine.add_rule('facts',
    ('is_furry', 'Erin'),
    (),
    ())

engine.add_rule('facts',
    ('is_white', 'Erin'),
    (),
    ())

engine.add_rule('facts',
    ('is_smart', 'Fiona'),
    (),
    ())

engine.add_rule('facts',
    ('is_white', 'Fiona'),
    (),
    ())

engine.add_rule('facts',
    ('is_young', 'Fiona'),
    (),
    ())

# Add inference rules
engine.add_rule('rules',
    ('is_young', '$thing'),
    (('is_nice', '$thing'), ('is_smart', '$thing')),
    ())

engine.add_rule('rules',
    ('is_cold', '$thing'),
    (('is_young', '$thing'), ('is_white', '$thing')),
    ())

engine.add_rule('rules',
    ('is_red', '$thing'),
    (('is_white', '$thing'),),
    ())

engine.add_rule('rules',
    ('is_nice', '$thing'),
    (('is_furry', '$thing'), ('is_red', '$thing')),
    ())

engine.add_rule('rules',
    ('is_white', '$thing'),
    (('is_young', '$thing'),),
    ())

engine.add_rule('rules',
    ('is_furry', '$thing'),
    (('is_smart', '$thing'), ('is_cold', '$thing')),
    ())

engine.add_rule('rules',
    ('is_smart', '$thing'),
    (('is_nice', '$thing'), ('is_white', '$thing')),
    ())

engine.add_rule('rules',
    ('is_red', 'Anne'),
    (('is_furry', 'Anne'), ('is_white', 'Anne')),
    ())

# Activate the engine
engine.activate('facts')

# Query: Is Erin cold?
try:
    result = list(engine.prove(('is_cold', 'Erin')))
    print("Erin is cold:", len(result) > 0)
except Exception as e:
    print(f"Error: {e}")