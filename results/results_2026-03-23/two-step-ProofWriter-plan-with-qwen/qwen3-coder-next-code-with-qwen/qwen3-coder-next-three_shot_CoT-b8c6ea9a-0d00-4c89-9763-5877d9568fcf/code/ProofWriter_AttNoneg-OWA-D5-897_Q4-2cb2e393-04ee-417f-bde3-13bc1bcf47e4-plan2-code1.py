# Import required modules
from pyke import knowledge_engine

# Create knowledge engine instance
engine = knowledge_engine.engine(__file__)

# --- Facts Section ---
engine.add_predicate('is_nice', 'Anne', True)

engine.add_predicate('is_big', 'Bob', True)
engine.add_predicate('is_blue', 'Bob', True)
engine.add_predicate('is_cold', 'Bob', True)

engine.add_predicate('is_big', 'Charlie', True)
engine.add_predicate('is_cold', 'Charlie', True)
engine.add_predicate('is_nice', 'Charlie', True)
engine.add_predicate('is_young', 'Charlie', True)

engine.add_predicate('is_furry', 'Fiona', True)
engine.add_predicate('is_young', 'Fiona', True)

# --- Rules Section ---

# Rule: If someone is furry and nice then they are cold.
engine.add_rule(
    'furry_and_nice_is_cold',
    [('is_furry', '$person'),
     ('is_nice', '$person')],
    [('is_cold', '$person')]
)

# Rule: All blue, cold people are big.
engine.add_rule(
    'blue_and_cold_are_big',
    [('is_blue', '$person'),
     ('is_cold', '$person')],
    [('is_big', '$person')]
)

# Rule: If someone is nice then they are smart.
engine.add_rule(
    'nice_is_smart',
    [('is_nice', '$person')],
    [('is_smart', '$person')]
)

# Rule: All smart, big people are nice.
engine.add_rule(
    'smart_and_big_are_nice',
    [('is_smart', '$person'),
     ('is_big', '$person')],
    [('is_nice', '$person')]
)

# Rule: All smart people are blue.
engine.add_rule(
    'smart_are_blue',
    [('is_smart', '$person')],
    [('is_blue', '$person')]
)

# Rule: Blue, smart people are furry.
engine.add_rule(
    'blue_and_smart_are_furry',
    [('is_blue', '$person'),
     ('is_smart', '$person')],
    [('is_furry', '$person')]
)

# Rule: Furry, cold people are smart.
engine.add_rule(
    'furry_and_cold_are_smart',
    [('is_furry', '$person'),
     ('is_cold', '$person')],
    [('is_smart', '$person')]
)

# Rule: Cold people are big.
engine.add_rule(
    'cold_are_big',
    [('is_cold', '$person')],
    [('is_big', '$person')]
)

# --- Query Section ---
# First, activate the rules to ensure all inferences are made
engine.activate('bc_example')  # Using a generic activation name

# Check if Charlie is smart
result = engine.query(('is_smart', 'Charlie'))

# Output the result (for debugging purposes)
print("Query result for Charlie being smart:", result)

# Determine truth value of "Charlie is not smart"
if result:
    print("False")  # Charlie IS smart, so "Charlie is not smart" is FALSE
else:
    print("Unknown")  # We cannot prove Charlie is smart, so status is UNKNOWN