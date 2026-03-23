from pyke import knowledge_engine

engine = knowledge_engine.engine(__file__)

# Facts
engine.add_universal_fact('kb', 'chases', ('bald_eagle', 'cat'))
engine.add_universal_fact('kb', 'is_young', ('bald_eagle',))
engine.add_universal_fact('kb', 'chases', ('lion', 'bald_eagle'))
engine.add_universal_fact('kb', 'chases', ('lion', 'cat'))
engine.add_universal_fact('kb', 'eats', ('lion', 'bald_eagle'))
engine.add_universal_fact('kb', 'eats', ('lion', 'cat'))
engine.add_universal_fact('kb', 'chases', ('mouse', 'bald_eagle'))
engine.add_universal_fact('kb', 'chases', ('mouse', 'lion'))
engine.add_universal_fact('kb', 'eats', ('mouse', 'bald_eagle'))
engine.add_universal_fact('kb', 'is_young', ('mouse',))
engine.add_universal_fact('kb', 'is_rough', ('cat',))
engine.add_universal_fact('kb', 'is_young', ('cat',))
engine.add_universal_fact('kb', 'sees', ('cat', 'bald_eagle'))

# Rules
engine.add_universal_rule('kb', 'round_from_kind',
    ('is_kind', '?x'),
    ('is_round', '?x'))

engine.add_universal_rule('kb', 'round_from_chasing_eagle',
    ('chases', '?x', 'bald_eagle'),
    ('is_round', '?x'))

engine.add_universal_rule('kb', 'sees_eagle_from_round',
    ('is_round', '?x'),
    ('sees', '?x', 'bald_eagle'))

engine.add_universal_rule('kb', 'eats_eagle_from_chasing_cat',
    ('chases', '?x', 'cat'),
    ('chases', 'cat', 'bald_eagle'),
    ('eats', '?x', 'bald_eagle'))

engine.add_universal_rule('kb', 'cat_sees_lion_from_chasing_cat',
    ('chases', '?x', 'cat'),
    ('sees', 'cat', 'lion'))

engine.add_universal_rule('kb', 'chase_eagle_from_seeing_cat',
    ('sees', '?x', 'cat'),
    ('chases', '?x', 'bald_eagle'))

engine.add_universal_rule('kb', 'eagle_sees_lion',
    ('is_young', 'bald_eagle'),
    ('chases', 'bald_eagle', 'lion'),
    ('sees', 'bald_eagle', 'lion'))

engine.add_universal_rule('kb', 'eagle_eats_cat',
    ('eats', 'mouse', 'cat'),
    ('eats', 'mouse', 'bald_eagle'),
    ('eats', 'bald_eagle', 'cat'))

engine.add_universal_rule('kb', 'eagle_sees_from_x',
    ('sees', '?x', 'bald_eagle'),
    ('chases', '?x', 'cat'),
    ('sees', 'bald_eagle', '?x'))

# Query
engine.add_universal_fact('kb', 'query_sees_cat_lion', ('sees', 'cat', 'lion'))