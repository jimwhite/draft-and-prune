from pyke import knowledge_engine

engine = knowledge_engine.engine(__file__)

# Facts section
engine.add_universal_fact('facts', 'is_a', 'Fae', 'dumpus', True)

# Rules section
engine.add_rule('tumpus_is_orange',
    ('is_a', '$thing', 'tumpus'),
    ('is_orange', '$thing'))

engine.add_rule('tumpus_is_numpus',
    ('is_a', '$thing', 'tumpus'),
    ('is_a', '$thing', 'numpus'))

engine.add_rule('numpus_is_small',
    ('is_a', '$thing', 'numpus'),
    ('is_small', '$thing'))

engine.add_rule('numpus_is_vumpus',
    ('is_a', '$thing', 'numpus'),
    ('is_a', '$thing', 'vumpus'))

engine.add_rule('vumpus_is_sour',
    ('is_a', '$thing', 'vumpus'),
    ('is_sour', '$thing'))

engine.add_rule('vumpus_is_dumpus',
    ('is_a', '$thing', 'vumpus'),
    ('is_a', '$thing', 'dumpus'))

engine.add_rule('dumpus_is_cold',
    ('is_a', '$thing', 'dumpus'),
    ('is_cold', '$thing'))

engine.add_rule('dumpus_is_zumpus',
    ('is_a', '$thing', 'dumpus'),
    ('is_a', '$thing', 'zumpus'))

engine.add_rule('zumpus_is_dull',
    ('is_a', '$thing', 'zumpus'),
    ('is_dull', '$thing'))

engine.add_rule('zumpus_is_yumpus',
    ('is_a', '$thing', 'zumpus'),
    ('is_a', '$thing', 'yumpus'))

engine.add_rule('jompus_is_floral',
    ('is_a', '$thing', 'jompus'),
    ('is_floral', '$thing'))

engine.add_rule('yumpus_is_not_amenable',
    ('is_a', '$thing', 'yumpus'),
    ('not', ('is_amenable', '$thing')))

engine.add_rule('yumpus_is_rompus',
    ('is_a', '$thing', 'yumpus'),
    ('is_a', '$thing', 'rompus'))

engine.add_rule('rompus_is_opaque',
    ('is_a', '$thing', 'rompus'),
    ('is_opaque', '$thing'))

engine.add_rule('rompus_is_impus',
    ('is_a', '$thing', 'rompus'),
    ('is_a', '$thing', 'impus'))

engine.add_rule('impus_is_not_floral',
    ('is_a', '$thing', 'impus'),
    ('not', ('is_floral', '$thing')))

engine.add_rule('impus_is_wumpus',
    ('is_a', '$thing', 'impus'),
    ('is_a', '$thing', 'wumpus'))

# Query section
try:
    result = engine.prove_1('facts', 'is_floral', ('Fae',), 1)
    # If prove_1 succeeds, it means is_floral(Fae) is true
    # So "Fae is not floral" would be false
    print("False" if result else "True")
except:
    # If prove_1 fails, it means is_floral(Fae) cannot be proven true
    # Given the rules, this should mean Fae is not floral
    print("True")