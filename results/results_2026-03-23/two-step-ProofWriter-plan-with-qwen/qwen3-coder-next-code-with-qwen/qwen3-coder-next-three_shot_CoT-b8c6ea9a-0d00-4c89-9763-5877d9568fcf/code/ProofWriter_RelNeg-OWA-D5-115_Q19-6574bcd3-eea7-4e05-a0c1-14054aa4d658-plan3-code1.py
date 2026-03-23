from pyke import knowledge_engine

# Create knowledge engine instance
engine = knowledge_engine.engine(__file__)

# --- Facts ---
engine.add_casefact('facts', 'is_blue', ('bald_eagle', True))
engine.add_casefact('facts', 'is_red', ('bald_eagle', True))
engine.add_casefact('facts', 'likes', ('bald_eagle', 'lion', True))
engine.add_casefact('facts', 'needs', ('bald_eagle', 'bear', True))
engine.add_casefact('facts', 'needs', ('bald_eagle', 'dog', True))
engine.add_casefact('facts', 'is_blue', ('bear', False))
engine.add_casefact('facts', 'is_nice', ('bear', True))
engine.add_casefact('facts', 'needs', ('bear', 'dog', True))
engine.add_casefact('facts', 'chases', ('dog', 'bald_eagle', True))
engine.add_casefact('facts', 'is_red', ('dog', True))
engine.add_casefact('facts', 'needs', ('dog', 'bear', False))
engine.add_casefact('facts', 'likes', ('lion', 'bear', False))

# --- Rules ---
engine.add_rule('likes_lion_not_red_chases_lion',
    ('facts.likes', '$x', 'lion', True),
    ('not', ('facts.is_red', '$x', True)),
    ('facts.chases', '$x', 'lion', True))

engine.add_rule('red_and_needs_bald_eagle_bald_eagle_needs_lion',
    ('facts.is_red', '$x', True),
    ('facts.needs', '$x', 'bald_eagle', True),
    ('facts.needs', 'bald_eagle', 'lion', True))

engine.add_rule('round_not_likes_dog',
    ('facts.is_round', '$x', True),
    ('not', ('facts.likes', '$x', 'dog', True)))

engine.add_rule('bald_eagle_needs_dog_dog_is_round',
    ('facts.needs', 'bald_eagle', 'dog', True),
    ('facts.is_round', 'dog', True))

engine.add_rule('likes_dog_likes_bald_eagle',
    ('facts.likes', '$x', 'dog', True),
    ('facts.likes', '$x', 'bald_eagle', True))

engine.add_rule('chases_lion_and_lion_likes_dog_dog_not_likes_lion',
    ('facts.chases', '$x', 'lion', True),
    ('facts.likes', 'lion', 'dog', True),
    ('not', ('facts.likes', 'dog', 'lion', True)))

engine.add_rule('bear_likes_lion_lion_likes_dog',
    ('facts.likes', 'bear', 'lion', True),
    ('facts.likes', 'lion', 'dog', True))

engine.add_rule('likes_bear_bear_likes_lion',
    ('facts.likes', '$x', 'bear', True),
    ('facts.likes', 'bear', 'lion', True))

engine.add_rule('round_likes_bear',
    ('facts.is_round', '$x', True),
    ('facts.likes', '$x', 'bear', True))

# --- Query ---
engine.activate('facts')
result = engine.prove('facts.needs', ('dog', 'dog', False), 1)
print(result is not None)