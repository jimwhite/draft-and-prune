from pyke import knowledge_engine

# --- Knowledge Base Setup ---
engine = knowledge_engine.engine(__file__)

# --- Facts ---
engine.add_case_fact('facts', ('is_furry', 'Anne', True))
engine.add_case_fact('facts', ('is_furry', 'Bob', True))
engine.add_case_fact('facts', ('is_blue', 'Gary', True))
engine.add_case_fact('facts', ('is_cold', 'Gary', True))
engine.add_case_fact('facts', ('is_furry', 'Gary', True))
engine.add_case_fact('facts', ('is_quiet', 'Gary', True))
engine.add_case_fact('facts', ('is_round', 'Gary', True))
engine.add_case_fact('facts', ('is_blue', 'Harry', True))
engine.add_case_fact('facts', ('is_cold', 'Harry', True))
engine.add_case_fact('facts', ('is_quiet', 'Harry', True))
engine.add_case_fact('facts', ('is_round', 'Harry', True))
engine.add_case_fact('facts', ('is_young', 'Harry', True))

# --- Rules ---
engine.add_rule('rules', 'cold_blue_quiet', 
    (('is_cold', '?x', True), ('is_blue', '?x', True)),
    (('is_quiet', '?x', True),))

engine.add_rule('rules', 'round_furry_quiet',
    (('is_round', '?x', True), ('is_furry', '?x', True)),
    (('is_quiet', '?x', True),))

engine.add_rule('rules', 'bob_blue_round_young',
    (('is_blue', 'Bob', True), ('is_round', 'Bob', True)),
    (('is_young', 'Bob', True),))

engine.add_rule('rules', 'round_blue',
    (('is_round', '?x', True),),
    (('is_blue', '?x', True),))

engine.add_rule('rules', 'young_round_blue',
    (('is_young', '?x', True), ('is_round', '?x', True)),
    (('is_blue', '?x', True),))

engine.add_rule('rules', 'harry_quiet_furry_blue',
    (('is_quiet', 'Harry', True), ('is_furry', 'Harry', True)),
    (('is_blue', 'Harry', True),))

engine.add_rule('rules', 'furry_cold',
    (('is_furry', '?x', True),),
    (('is_cold', '?x', True),))

engine.add_rule('rules', 'cold_round',
    (('is_cold', '?x', True),),
    (('is_round', '?x', True),))

engine.add_rule('rules', 'young_furry_rough',
    (('is_young', '?x', True), ('is_furry', '?x', True)),
    (('is_rough', '?x', True),))

# --- Activate and Run ---
engine.activate('rules')

# --- Query ---
result = engine.query(('is_furry', 'Harry', True))
print("Harry is furry:", result)