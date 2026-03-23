from pyke import knowledge_engine

# Initialize the knowledge engine
engine = knowledge_engine.engine(__file__)

# Facts: explicitly stated properties and relationships
engine.add_universal_fact('kb', 'eats', ('bear', 'squirrel'))
engine.add_universal_fact('kb', 'is_cold', ('bear',))
engine.add_universal_fact('kb', 'is_rough', ('bear',))
engine.add_universal_fact('kb', 'visits', ('bear', 'lion'))
engine.add_universal_fact('kb', 'eats', ('cat', 'lion'))
engine.add_universal_fact('kb', 'likes', ('lion', 'cat'))
engine.add_universal_fact('kb', 'visits', ('lion', 'bear'))
engine.add_universal_fact('kb', 'eats', ('squirrel', 'lion'))
engine.add_universal_fact('kb', 'is_cold', ('squirrel',))
engine.add_universal_fact('kb', 'is_rough', ('squirrel',))
engine.add_universal_fact('kb', 'likes', ('squirrel', 'bear'))
engine.add_universal_fact('kb', 'visits', ('squirrel', 'lion'))
engine.add_universal_fact('kb', 'is_green', ('red_people',))

# Rules: conditional logic
engine.add_universal_rule('kb',
    'eats_lion_red',
    ('squirrel',),
    ('someone',),
    ('eats', 'someone', 'lion'),
    ('is_red', 'lion',)
)

engine.add_universal_rule('kb',
    'green_likes_lion_eats_bear',
    ('squirrel',),
    ('someone',),
    ('is_green', 'someone'),
    ('likes', 'someone', 'lion'),
    ('eats', 'someone', 'bear')
)

engine.add_universal_rule('kb',
    'visits_bear_bear_likes_lion',
    ('squirrel',),
    ('someone',),
    ('visits', 'someone', 'bear'),
    ('likes', 'bear', 'lion')
)

engine.add_universal_rule('kb',
    'likes_squirrel_and_lion_visits_lion',
    ('squirrel',),
    ('someone',),
    ('likes', 'someone', 'squirrel'),
    ('likes', 'someone', 'lion'),
    ('visits', 'someone', 'lion')
)

engine.add_universal_rule('kb',
    'green_eats_squirrel',
    ('squirrel',),
    ('someone',),
    ('is_green', 'someone'),
    ('eats', 'someone', 'squirrel')
)

engine.add_universal_rule('kb',
    'likes_lion_visits_bear',
    ('squirrel',),
    ('someone',),
    ('likes', 'someone', 'lion'),
    ('visits', 'someone', 'bear')
)

engine.add_universal_rule('kb',
    'visits_lion_green_lion_is_red',
    ('squirrel',),
    ('someone',),
    ('visits', 'someone', 'lion'),
    ('is_green', 'lion'),
    ('is_red', 'someone')
)

# Query: is the squirrel not rough?
# We need to check if is_rough('squirrel') is false
# Since we have is_rough('squirrel') as a fact, the statement "squirrel is not rough" is false
query = engine.add_query('kb', 'is_rough', ('squirrel',))

# Run the engine
engine.activate('kb')

# Execute query to check if is_rough(squirrel) holds
result = list(query())
is_squirrel_rough = len(result) > 0

# The statement "The squirrel is not rough" is equivalent to NOT is_rough(squirrel)
statement_true = not is_squirrel_rough

print("The squirrel is rough:", is_squirrel_rough)
print("Statement 'squirrel is not rough' is:", statement_true)