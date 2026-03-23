# PyKe program for the animal logic puzzle

from pyke import knowledge_engine

engine = knowledge_engine.engine(__name__)

# --- Facts ---
engine.add_case_fact('facts', 'eats', ('cow', 'lion', True))
engine.add_case_fact('facts', 'eats', ('lion', 'mouse', True))
engine.add_case_fact('facts', 'needs', ('lion', 'mouse', True))
engine.add_case_fact('facts', 'sees', ('mouse', 'lion', True))
engine.add_case_fact('facts', 'eats', ('tiger', 'lion', True))
engine.add_case_fact('facts', 'is_green', ('tiger', True))
engine.add_case_fact('facts', 'is_red', ('tiger', True))
engine.add_case_fact('facts', 'needs', ('tiger', 'lion', True))
engine.add_case_fact('facts', 'needs', ('tiger', 'mouse', True))
engine.add_case_fact('facts', 'sees', ('tiger', 'cow', True))

# --- Rules ---
engine.add_rule(
    'sees_lion_is_cold',
    ('facts.sees', '$person', 'lion', True),
    ('facts.is_cold', '$person', True)
)

engine.add_rule(
    'needs_tiger_and_mouse_is_cold',
    [('facts.needs', '$person', 'tiger', True),
     ('facts.needs', '$person', 'mouse', True)],
    ('facts.is_cold', '$person', True)
)

engine.add_rule(
    'needs_tiger_and_tiger_eats_cow_tiger_needs_lion',
    [('facts.needs', '$person', 'tiger', True),
     ('facts.eats', 'tiger', 'cow', True)],
    ('facts.needs', 'tiger', 'lion', True)
)

engine.add_rule(
    'round_are_green',
    ('facts.is_round', '$person', True),
    ('facts.is_green', '$person', True)
)

engine.add_rule(
    'young_and_green_are_round',
    [('facts.is_young', '$person', True),
     ('facts.is_green', '$person', True)],
    ('facts.is_round', '$person', True)
)

engine.add_rule(
    'eats_mouse_and_mouse_sees_lion_is_green',
    [('facts.eats', '$person', 'mouse', True),
     ('facts.sees', 'mouse', 'lion', True)],
    ('facts.is_green', '$person', True)
)

engine.add_rule(
    'needs_tiger_tiger_sees_lion',
    ('facts.needs', '$person', 'tiger', True),
    ('facts.sees', 'tiger', 'lion', True)
)

engine.add_rule(
    'cold_and_sees_lion_needs_tiger',
    [('facts.is_cold', '$person', True),
     ('facts.sees', '$person', 'lion', True)],
    ('facts.needs', '$person', 'tiger', True)
)

# --- Query ---
engine.activate('rules')

try:
    result = list(engine.prove('facts', 'needs', ('cow', 'tiger', True), 1))
    if result:
        print("The statement 'the cow needs the tiger' is: true")
    else:
        print("The statement 'the cow needs the tiger' is: false")
except Exception as e:
    print(f"Error: {e}")