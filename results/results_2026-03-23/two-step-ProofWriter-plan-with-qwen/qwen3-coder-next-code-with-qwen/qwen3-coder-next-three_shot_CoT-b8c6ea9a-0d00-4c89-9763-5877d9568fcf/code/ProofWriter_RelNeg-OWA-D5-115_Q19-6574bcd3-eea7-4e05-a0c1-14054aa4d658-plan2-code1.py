from pyke import knowledge_engine

engine = knowledge_engine.engine(__file__)

# Facts
engine.add_rule('facts', 'is_blue', ('bald_eagle',), True)
engine.add_rule('facts', 'is_red', ('bald_eagle',), True)
engine.add_rule('facts', 'likes', ('bald_eagle', 'lion'), True)
engine.add_rule('facts', 'needs', ('bald_eagle', 'bear'), True)
engine.add_rule('facts', 'needs', ('bald_eagle', 'dog'), True)
engine.add_rule('facts', 'is_blue', ('bear',), False)  # bear is not blue
engine.add_rule('facts', 'is_nice', ('bear',), True)
engine.add_rule('facts', 'needs', ('bear', 'dog'), True)
engine.add_rule('facts', 'chases', ('dog', 'bald_eagle'), True)
engine.add_rule('facts', 'is_red', ('dog',), True)
engine.add_rule('facts', 'needs', ('dog', 'bear'), False)  # dog does not need bear
engine.add_rule('facts', 'likes', ('lion', 'bear'), False)  # lion does not like bear

# Rules
engine.add_rule('rules', 'chase_lion_if_likes_and_not_red',
    (('likes', '?x', 'lion'), ('not', ('is_red', '?x'))),
    ('chases', '?x', 'lion'))

engine.add_rule('rules', 'bald_eagle_needs_lion_if_red_and_needs_bald_eagle',
    (('is_red', '?x'), ('needs', '?x', 'bald_eagle')),
    ('needs', 'bald_eagle', 'lion'))

engine.add_rule('rules', 'not_likes_dog_if_round',
    ('is_round', '?x'),
    ('not', ('likes', '?x', 'dog')))

engine.add_rule('rules', 'dog_is_round_if_bald_eagle_needs_dog',
    ('needs', 'bald_eagle', 'dog'),
    ('is_round', 'dog'))

engine.add_rule('rules', 'likes_bald_eagle_if_likes_dog',
    ('likes', '?x', 'dog'),
    ('likes', '?x', 'bald_eagle'))

engine.add_rule('rules', 'dog_not_likes_lion_if_chases_lion_and_lion_likes_dog',
    (('chases', '?x', 'lion'), ('likes', 'lion', 'dog')),
    ('not', ('likes', 'dog', 'lion')))

engine.add_rule('rules', 'lion_likes_dog_if_bear_likes_lion',
    ('likes', 'bear', 'lion'),
    ('likes', 'lion', 'dog'))

engine.add_rule('rules', 'bear_likes_lion_if_any_likes_bear',
    ('likes', '?x', 'bear'),
    ('likes', 'bear', 'lion'))

engine.add_rule('rules', 'likes_bear_if_round',
    ('is_round', '?x'),
    ('likes', '?x', 'bear'))

# Query: The dog does not need the dog
query = engine.add_goal(('needs', 'dog', 'dog'))

# Since we need to check if needs("dog", "dog") is False, 
# we'll query for the negation
engine.add_goal(('not', ('needs', 'dog', 'dog')))