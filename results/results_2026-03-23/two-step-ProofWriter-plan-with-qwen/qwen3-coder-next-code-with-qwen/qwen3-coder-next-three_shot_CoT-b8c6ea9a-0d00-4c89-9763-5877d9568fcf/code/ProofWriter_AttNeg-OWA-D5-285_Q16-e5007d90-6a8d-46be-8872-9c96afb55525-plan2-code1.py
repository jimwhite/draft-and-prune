# Import required modules
from pyke import knowledge_engine

# Create knowledge engine instance
engine = knowledge_engine.engine(__file__)

# --- Facts ---
engine.add_case_fact('kb', ('is_big', 'Bob', True))
engine.add_case_fact('kb', ('is_cold', 'Bob', True))
engine.add_case_fact('kb', ('is_furry', 'Bob', True))
engine.add_case_fact('kb', ('is_smart', 'Bob', True))

engine.add_case_fact('kb', ('is_cold', 'Fiona', True))
engine.add_case_fact('kb', ('is_green', 'Fiona', False))
engine.add_case_fact('kb', ('is_white', 'Fiona', True))

engine.add_case_fact('kb', ('is_smart', 'Gary', True))

engine.add_case_fact('kb', ('is_big', 'Harry', True))
engine.add_case_fact('kb', ('is_cold', 'Harry', True))
engine.add_case_fact('kb', ('is_smart', 'Harry', True))

# --- Rules ---
# All green people are furry.
engine.add_rule('kb', 
    ('is_green', '?x', True),
    (),
    ('is_furry', '?x', True))

# If Gary is furry and Gary is not smart then Gary is white.
engine.add_rule('kb',
    ('is_furry', 'Gary', True),
    (('is_smart', 'Gary', False),),
    ('is_white', 'Gary', True))

# Smart people are green.
engine.add_rule('kb',
    ('is_smart', '?x', True),
    (),
    ('is_green', '?x', True))

# If Bob is not green and Bob is not white then Bob is furry.
engine.add_rule('kb',
    (('is_green', 'Bob', False),),
    (('is_white', 'Bob', False),),
    ('is_furry', 'Bob', True))

# Big people are cold.
engine.add_rule('kb',
    ('is_big', '?x', True),
    (),
    ('is_cold', '?x', True))

# If someone is smart and furry then they are big.
engine.add_rule('kb',
    ('is_smart', '?x', True),
    (('is_furry', '?x', True),),
    ('is_big', '?x', True))

# If someone is white and not cold then they are not blue.
engine.add_rule('kb',
    ('is_white', '?x', True),
    (('is_cold', '?x', False),),
    ('is_blue', '?x', False))

# All cold people are not blue.
engine.add_rule('kb',
    ('is_cold', '?x', True),
    (),
    ('is_blue', '?x', False))

# --- Query ---
# Check if Bob is white
result = engine.prove_1('kb', ('is_white', 'Bob', True), None)

print("Bob is white:", result is not None)