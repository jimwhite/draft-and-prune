# Import required modules
from pyke import knowledge_engine

# Create knowledge engine instance
engine = knowledge_engine.engine(__file__)

# The facts, rules, and query should be in separate .krb files
# But since we need everything in one file, we'll use the Python API correctly

# --- Facts about individuals ---
engine.add_case_fact('facts', ('is_cold', 'Bob', True))
engine.add_case_fact('facts', ('is_quiet', 'Bob', True))
engine.add_case_fact('facts', ('is_red', 'Bob', True))
engine.add_case_fact('facts', ('is_smart', 'Bob', True))

engine.add_case_fact('facts', ('is_kind', 'Charlie', True))
engine.add_case_fact('facts', ('is_quiet', 'Charlie', True))
engine.add_case_fact('facts', ('is_red', 'Charlie', True))
engine.add_case_fact('facts', ('is_rough', 'Charlie', True))

engine.add_case_fact('facts', ('is_cold', 'Dave', True))
engine.add_case_fact('facts', ('is_kind', 'Dave', True))
engine.add_case_fact('facts', ('is_smart', 'Dave', True))

engine.add_case_fact('facts', ('is_quiet', 'Fiona', True))

# --- Rules ---

# Rule: If something is quiet and cold then it is smart.
engine.add_rule('quiet_and_cold_is_smart', 
    ( ('facts', 'is_quiet', '$x'),
      ('facts', 'is_cold', '$x') ),
    ( ('facts', 'is_smart', '$x'), ))

# Rule: Red and cold things are round.
engine.add_rule('red_and_cold_are_round', 
    ( ('facts', 'is_red', '$x'),
      ('facts', 'is_cold', '$x') ),
    ( ('facts', 'is_round', '$x'), ))

# Rule: If something is kind and rough then it is red.
engine.add_rule('kind_and_rough_is_red', 
    ( ('facts', 'is_kind', '$x'),
      ('facts', 'is_rough', '$x') ),
    ( ('facts', 'is_red', '$x'), ))

# Rule: All quiet things are rough.
engine.add_rule('quiet_are_rough', 
    ( ('facts', 'is_quiet', '$x'), ),
    ( ('facts', 'is_rough', '$x'), ))

# Rule: Cold and smart things are red.
engine.add_rule('cold_and_smart_are_red', 
    ( ('facts', 'is_cold', '$x'),
      ('facts', 'is_smart', '$x') ),
    ( ('facts', 'is_red', '$x'), ))

# Rule: If something is rough then it is cold.
engine.add_rule('rough_is_cold', 
    ( ('facts', 'is_rough', '$x'), ),
    ( ('facts', 'is_cold', '$x'), ))

# Rule: All red things are rough.
engine.add_rule('red_are_rough', 
    ( ('facts', 'is_red', '$x'), ),
    ( ('facts', 'is_rough', '$x'), ))

# Rule: If Dave is smart and Dave is kind then Dave is quiet.
engine.add_rule('dave_smart_and_kind_is_quiet', 
    ( ('facts', 'is_smart', 'Dave'),
      ('facts', 'is_kind', 'Dave') ),
    ( ('facts', 'is_quiet', 'Dave'), ))

# Activate the knowledge base
engine.activate('bc_example')  # Usually needs a specific activation name

# --- Query: Is Charlie kind? ---
try:
    result = engine.query(('facts', 'is_kind', 'Charlie'))
    print(result)
except Exception as e:
    # If direct query fails, try to prove it through backward chaining
    engine.activate('bc_example')
    plan = engine.prove(('facts', 'is_kind', 'Charlie'), 1)
    print(plan is not None)