from pyke import knowledge_engine

engine = knowledge_engine.engine(__file__)

# Facts
engine.add_rule('facts', 'eats', ('bear', 'squirrel', True))
engine.add_rule('facts', 'is_cold', ('bear', True))
engine.add_rule('facts', 'is_rough', ('bear', True))
engine.add_rule('facts', 'visits', ('bear', 'lion', True))

engine.add_rule('facts', 'eats', ('cat', 'lion', True))
engine.add_rule('facts', 'likes', ('lion', 'cat', True))

engine.add_rule('facts', 'visits', ('lion', 'bear', True))
# Note: likes("lion", "cat", True) already added above

engine.add_rule('facts', 'eats', ('squirrel', 'lion', True))
engine.add_rule('facts', 'is_cold', ('squirrel', True))
engine.add_rule('facts', 'is_rough', ('squirrel', True))
engine.add_rule('facts', 'likes', ('squirrel', 'bear', True))
engine.add_rule('facts', 'visits', ('squirrel', 'lion', True))

# Rules
engine.add_rule('rules', 'eats_lion_makes_lion_red',
    (lambda: [('?x', '?lion')] if engine.prove1('facts', 'eats', ('?x', 'lion', True)) else None),
    lambda ?x, ?lion: engine.add_rule('facts', 'red', ('lion', True)))

engine.add_rule('rules', 'green_and_likes_lion_eats_bear',
    (lambda: [('?x')] if engine.prove1('facts', 'is_green', ('?x', True)) and 
                engine.prove1('facts', 'likes', ('?x', 'lion', True)) else None),
    lambda ?x: engine.add_rule('facts', 'eats', ('?x', 'bear', True)))

engine.add_rule('rules', 'visits_bear_makes_bear_like_lion',
    (lambda: [('?x')] if engine.prove1('facts', 'visits', ('?x', 'bear', True)) else None),
    lambda ?x: engine.add_rule('facts', 'likes', ('bear', 'lion', True)))

engine.add_rule('rules', 'likes_squirrel_and_lion_visits_lion',
    (lambda: [('?x')] if engine.prove1('facts', 'likes', ('?x', 'squirrel', True)) and 
                engine.prove1('facts', 'likes', ('?x', 'lion', True)) else None),
    lambda ?x: engine.add_rule('facts', 'visits', ('?x', 'lion', True)))

engine.add_rule('rules', 'green_eats_squirrel',
    (lambda: [('?x')] if engine.prove1('facts', 'is_green', ('?x', True)) else None),
    lambda ?x: engine.add_rule('facts', 'eats', ('?x', 'squirrel', True)))

engine.add_rule('rules', 'likes_lion_visits_bear',
    (lambda: [('?x')] if engine.prove1('facts', 'likes', ('?x', 'lion', True)) else None),
    lambda ?x: engine.add_rule('facts', 'visits', ('?x', 'bear', True)))

engine.add_rule('rules', 'visits_lion_and_red_lion_makes_self_red',
    (lambda: [('?x')] if engine.prove1('facts', 'visits', ('?x', 'lion', True)) and 
                engine.prove1('facts', 'red', ('lion', True)) else None),
    lambda ?x: engine.add_rule('facts', 'red', ('?x', True)))

# Query
result = engine.prove1('facts', 'is_rough', ('squirrel', False))
print("Result:", result)