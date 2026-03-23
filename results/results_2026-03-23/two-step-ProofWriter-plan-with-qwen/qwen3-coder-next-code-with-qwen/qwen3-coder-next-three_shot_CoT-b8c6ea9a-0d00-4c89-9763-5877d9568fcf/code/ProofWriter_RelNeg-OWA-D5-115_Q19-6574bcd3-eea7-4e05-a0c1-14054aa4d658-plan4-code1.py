from pyke import knowledge_engine

# Create knowledge base
engine = knowledge_engine.engine(__file__)

# Facts
engine.add_rule('facts', 'is_blue', ('bald_eagle', True), None)
engine.add_rule('facts', 'is_red', ('bald_eagle', True), None)
engine.add_rule('facts', 'likes', ('bald_eagle', 'lion', True), None)
engine.add_rule('facts', 'needs', ('bald_eagle', 'bear', True), None)
engine.add_rule('facts', 'needs', ('bald_eagle', 'dog', True), None)
engine.add_rule('facts', 'is_blue', ('bear', False), None)
engine.add_rule('facts', 'is_nice', ('bear', True), None)
engine.add_rule('facts', 'needs', ('bear', 'dog', True), None)
engine.add_rule('facts', 'chases', ('dog', 'bald_eagle', True), None)
engine.add_rule('facts', 'is_red', ('dog', True), None)
engine.add_rule('facts', 'needs', ('dog', 'bear', False), None)
engine.add_rule('facts', 'likes', ('lion', 'bear', False), None)

# Rules
engine.add_rule('rules', 'chases_lion_if_likes_and_not_red',
    (('likes', '?x', 'lion', True), ('is_red', '?x', False)),
    ('chases', '?x', 'lion', True))

engine.add_rule('rules', 'bald_eagle_needs_lion_if_red_and_needs_bald_eagle',
    (('is_red', '?x', True), ('needs', '?x', 'bald_eagle', True)),
    ('needs', 'bald_eagle', 'lion', True))

engine.add_rule('rules', 'round_implies_not_likes_dog',
    (('is_round', '?x', True),),
    ('likes', '?x', 'dog', False))

engine.add_rule('rules', 'bald_eagle_needs_dog_implies_dog_round',
    (('needs', 'bald_eagle', 'dog', True),),
    ('is_round', 'dog', True))

engine.add_rule('rules', 'likes_dog_implies_likes_bald_eagle',
    (('likes', '?x', 'dog', True),),
    ('likes', '?x', 'bald_eagle', True))

engine.add_rule('rules', 'chases_lion_and_lion_likes_dog_implies_dog_not_likes_lion',
    (('chases', '?x', 'lion', True), ('likes', 'lion', 'dog', True)),
    ('likes', 'dog', 'lion', False))

engine.add_rule('rules', 'bear_likes_lion_implies_lion_likes_dog',
    (('likes', 'bear', 'lion', True),),
    ('likes', 'lion', 'dog', True))

engine.add_rule('rules', 'likes_bear_implies_bear_likes_lion',
    (('likes', '?x', 'bear', True),),
    ('likes', 'bear', 'lion', True))

engine.add_rule('rules', 'round_implies_likes_bear',
    (('is_round', '?x', True),),
    ('likes', '?x', 'bear', True))

# Query
engine.add_rule('query', 'needs_dog_not_need_self',
    (),
    ('needs', 'dog', 'dog', False))

# Run inference
engine.activate('facts')
engine.activate('rules')

try:
    result = engine.prove(('needs', 'dog', 'dog', False), 1)
    print("True" if result else "False")
except:
    # If we can't prove it, check if we can disprove
    try:
        result = engine.prove(('needs', 'dog', 'dog', True), 1)
        print("False" if result else "Unknown")
    except:
        print("Unknown")