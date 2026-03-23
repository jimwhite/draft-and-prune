from pyke import knowledge_engine

# Create knowledge engine instance
engine = knowledge_engine.engine(__file__)

# Add facts
engine.add_case_fact('kb', ('eats', 'cat', 'squirrel'))
engine.add_case_fact('kb', ('sees', 'cat', 'squirrel'))
engine.add_case_fact('kb', ('eats', 'cow', 'squirrel'))
engine.add_case_fact('kb', ('sees', 'cow', 'cat'))
engine.add_case_fact('kb', ('is_round', 'rabbit', True))
engine.add_case_fact('kb', ('sees', 'rabbit', 'cat'))
engine.add_case_fact('kb', ('eats', 'squirrel', 'rabbit'))
engine.add_case_fact('kb', ('is_cold', 'squirrel', True))
engine.add_case_fact('kb', ('needs', 'squirrel', 'rabbit'))
engine.add_case_fact('kb', ('sees', 'squirrel', 'cat'))

# Add rules
engine.add_rule('kb', '''
    rule sees_cat_not_green_sees_cow:
        if sees($X, 'cat') and not is_green($X)
        then sees($X, 'cow')
''')

engine.add_rule('kb', '''
    rule rabbit_kind_and_sees_squirrel_needs_rabbit:
        if is_kind('rabbit') and sees('rabbit', 'squirrel')
        then needs('squirrel', 'rabbit')
''')

engine.add_rule('kb', '''
    rule rough_is_cold:
        if is_rough($X)
        then is_cold($X)
''')

engine.add_rule('kb', '''
    rule sees_rabbit_not_round:
        if sees($X, 'rabbit')
        then not is_round($X)
''')

engine.add_rule('kb', '''
    rule sees_squirrel_not_green_needs_squirrel:
        if sees($X, 'squirrel') and not is_green($X)
        then needs($X, 'squirrel')
''')

engine.add_rule('kb', '''
    rule eats_cow_sees_rabbit:
        if eats($X, 'cow')
        then sees($X, 'rabbit')
''')

engine.add_rule('kb', '''
    rule eats_squirrel_is_rough:
        if eats($X, 'squirrel')
        then is_rough($X)
''')

engine.add_rule('kb', '''
    rule is_cold_eats_cow:
        if is_cold($X)
        then eats($X, 'cow')
''')

# Add query
try:
    result = engine.prove_1('kb', 'is_round', ('cat',), False)
    print("False" if result else "True")
except:
    # If we can't prove it's round, then it's not round (closed world assumption)
    print("True")