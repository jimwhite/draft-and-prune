from pyke import knowledge_engine

engine = knowledge_engine.engine(__file__)

# Facts
engine.add_rule('facts', 'is_blue', ('bald_eagle',), True)
engine.add_rule('facts', 'is_red', ('bald_eagle',), True)
engine.add_rule('facts', 'likes', ('bald_eagle', 'lion'), True)
engine.add_rule('facts', 'needs', ('bald_eagle', 'bear'), True)
engine.add_rule('facts', 'needs', ('bald_eagle', 'dog'), True)
engine.add_rule('facts', 'is_blue', ('bear',), False)
engine.add_rule('facts', 'is_nice', ('bear',), True)
engine.add_rule('facts', 'needs', ('bear', 'dog'), True)
engine.add_rule('facts', 'chases', ('dog', 'bald_eagle'), True)
engine.add_rule('facts', 'is_red', ('dog',), True)
engine.add_rule('facts', 'needs', ('dog', 'bear'), False)
engine.add_rule('facts', 'likes', ('lion', 'bear'), False)

# Rules
engine.add_rule('rules', 'chases_lion_if_likes_and_not_red',
    (('$x',), 'likes($x, lion)', '$x', 'is_red($x, False)'),
    ('$x',), 'chases($x, lion)')

engine.add_rule('rules', 'bald_eagle_needs_lion_if_red_and_needs_bald_eagle',
    (('$x',), 'is_red($x, True)', '$x', 'needs($x, bald_eagle)'),
    (), 'needs(bald_eagle, lion)')

engine.add_rule('rules', 'not_likes_dog_if_round',
    (('$x',), 'is_round($x, True)'),
    ('$x',), 'likes($x, dog, False)')

engine.add_rule('rules', 'dog_is_round_if_bald_eagle_needs_dog',
    (), 'needs(bald_eagle, dog)',
    (), 'is_round(dog)')

engine.add_rule('rules', 'likes_bald_eagle_if_likes_dog',
    (('$x',), 'likes($x, dog)'),
    ('$x',), 'likes($x, bald_eagle)')

engine.add_rule('rules', 'dog_not_likes_lion_if_chases_lion_and_lion_likes_dog',
    (('$x',), 'chases($x, lion)', '$x', 'likes(lion, dog)'),
    (), 'likes(dog, lion, False)')

engine.add_rule('rules', 'lion_likes_dog_if_bear_likes_lion',
    (), 'likes(bear, lion)',
    (), 'likes(lion, dog)')

engine.add_rule('rules', 'bear_likes_lion_if_something_likes_bear',
    (('$x',), 'likes($x, bear)'),
    (), 'likes(bear, lion)')

engine.add_rule('rules', 'likes_bear_if_round',
    (('$x',), 'is_round($x, True)'),
    ('$x',), 'likes($x, bear)')

# Query
engine.add_rule('query', 'dog_does_not_need_dog',
    (), 'needs(dog, dog, False)')

# Run the engine
engine.activate('rules')
result = engine.prove('query', 'dog_does_not_need_dog', 1)
print(result is not None)