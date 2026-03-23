from pyke import knowledge_engine

engine = knowledge_engine.engine(__file__)

# --- Facts ---
engine.add_universal_fact('facts', 'is_nice', ('Anne', True))
engine.add_universal_fact('facts', 'is_big', ('Bob', True))
engine.add_universal_fact('facts', 'is_blue', ('Bob', True))
engine.add_universal_fact('facts', 'is_cold', ('Bob', True))
engine.add_universal_fact('facts', 'is_big', ('Charlie', True))
engine.add_universal_fact('facts', 'is_cold', ('Charlie', True))
engine.add_universal_fact('facts', 'is_nice', ('Charlie', True))
engine.add_universal_fact('facts', 'is_young', ('Charlie', True))
engine.add_universal_fact('facts', 'is_furry', ('Fiona', True))
engine.add_universal_fact('facts', 'is_young', ('Fiona', True))

# --- Rules ---
engine.add_universal_rule('rules', 'furry_and_nice_implies_cold',
    (('is_furry', '?x', True),
     ('is_nice', '?x', True)),
    (('is_cold', '?x', True),))

engine.add_universal_rule('rules', 'bob_blue_and_big_implies_cold',
    (('is_blue', 'Bob', True),
     ('is_big', 'Bob', True)),
    (('is_cold', 'Bob', True),))

engine.add_universal_rule('rules', 'blue_and_cold_implies_big',
    (('is_blue', '?x', True),
     ('is_cold', '?x', True)),
    (('is_big', '?x', True),))

engine.add_universal_rule('rules', 'nice_implies_smart',
    (('is_nice', '?x', True),),
    (('is_smart', '?x', True),))

engine.add_universal_rule('rules', 'smart_and_big_implies_nice',
    (('is_smart', '?x', True),
     ('is_big', '?x', True)),
    (('is_nice', '?x', True),))

engine.add_universal_rule('rules', 'smart_implies_blue',
    (('is_smart', '?x', True),),
    (('is_blue', '?x', True),))

engine.add_universal_rule('rules', 'blue_and_smart_implies_furry',
    (('is_blue', '?x', True),
     ('is_smart', '?x', True)),
    (('is_furry', '?x', True),))

engine.add_universal_rule('rules', 'furry_and_cold_implies_smart',
    (('is_furry', '?x', True),
     ('is_cold', '?x', True)),
    (('is_smart', '?x', True),))

engine.add_universal_rule('rules', 'cold_implies_big',
    (('is_cold', '?x', True),),
    (('is_big', '?x', True),))

# --- Query ---
engine.activate('rules')
result = engine.prove(('facts', 'is_smart', ('Charlie', False)), 1)
print("Charlie is not smart:", result is None)  # If proof fails, statement is false