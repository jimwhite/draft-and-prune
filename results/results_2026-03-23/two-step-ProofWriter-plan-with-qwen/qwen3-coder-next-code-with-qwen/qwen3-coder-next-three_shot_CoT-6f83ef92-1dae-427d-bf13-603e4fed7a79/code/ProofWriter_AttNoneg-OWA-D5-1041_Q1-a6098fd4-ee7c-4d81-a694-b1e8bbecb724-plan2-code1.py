# Import required modules
from pyke import knowledge_engine

# Create knowledge engine instance
engine = knowledge_engine.engine(__file__)

# --- Facts about Bob ---
engine.add_case_fact('facts', ('is_cold', 'Bob', True))
engine.add_case_fact('facts', ('is_quiet', 'Bob', True))
engine.add_case_fact('facts', ('is_red', 'Bob', True))
engine.add_case_fact('facts', ('is_smart', 'Bob', True))

# --- Facts about Charlie ---
engine.add_case_fact('facts', ('is_kind', 'Charlie', True))
engine.add_case_fact('facts', ('is_quiet', 'Charlie', True))
engine.add_case_fact('facts', ('is_red', 'Charlie', True))
engine.add_case_fact('facts', ('is_rough', 'Charlie', True))

# --- Facts about Dave ---
engine.add_case_fact('facts', ('is_cold', 'Dave', True))
engine.add_case_fact('facts', ('is_kind', 'Dave', True))
engine.add_case_fact('facts', ('is_smart', 'Dave', True))

# --- Facts about Fiona ---
engine.add_case_fact('facts', ('is_quiet', 'Fiona', True))

# --- Rules ---

# Rule: If something is quiet and cold then it is smart.
engine.add_rule('quiet_and_cold_is_smart', 
    ( ('facts', 'is_quiet', '$thing', True),
      ('facts', 'is_cold', '$thing', True) ),
    ( ('facts', 'is_smart', '$thing', True), ))

# Rule: Red, cold things are round.
engine.add_rule('red_and_cold_are_round', 
    ( ('facts', 'is_red', '$thing', True),
      ('facts', 'is_cold', '$thing', True) ),
    ( ('facts', 'is_round', '$thing', True), ))

# Rule: If something is kind and rough then it is red.
engine.add_rule('kind_and_rough_is_red', 
    ( ('facts', 'is_kind', '$thing', True),
      ('facts', 'is_rough', '$thing', True) ),
    ( ('facts', 'is_red', '$thing', True), ))

# Rule: All quiet things are rough.
engine.add_rule('quiet_are_rough', 
    ( ('facts', 'is_quiet', '$thing', True), ),
    ( ('facts', 'is_rough', '$thing', True), ))

# Rule: Cold, smart things are red.
engine.add_rule('cold_and_smart_are_red', 
    ( ('facts', 'is_cold', '$thing', True),
      ('facts', 'is_smart', '$thing', True) ),
    ( ('facts', 'is_red', '$thing', True), ))

# Rule: If something is rough then it is cold.
engine.add_rule('rough_is_cold', 
    ( ('facts', 'is_rough', '$thing', True), ),
    ( ('facts', 'is_cold', '$thing', True), ))

# Rule: All red things are rough.
engine.add_rule('red_are_rough', 
    ( ('facts', 'is_red', '$thing', True), ),
    ( ('facts', 'is_rough', '$thing', True), ))

# Rule: If Dave is smart and Dave is kind then Dave is quiet.
engine.add_rule('dave_smart_and_kind_is_quiet', 
    ( ('facts', 'is_smart', 'Dave', True),
      ('facts', 'is_kind', 'Dave', True) ),
    ( ('facts', 'is_quiet', 'Dave', True), ))

# Activate the knowledge base and run inference
engine.activate('facts')

# --- Query: Is Charlie kind? ---
result = engine.query(('facts', 'is_kind', 'Charlie', True))

# Output the result
if result:
    print("True")
else:
    print("False")