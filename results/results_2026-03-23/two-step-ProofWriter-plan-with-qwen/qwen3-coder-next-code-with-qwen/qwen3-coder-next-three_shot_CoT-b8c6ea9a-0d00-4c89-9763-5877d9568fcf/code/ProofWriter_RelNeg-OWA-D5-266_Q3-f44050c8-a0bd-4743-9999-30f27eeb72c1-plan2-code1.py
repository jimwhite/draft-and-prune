from pyke import knowledge_engine

# Initialize the knowledge engine
engine = knowledge_engine.engine(__file__)

# --- Facts ---
engine.add_case_fact('kb', ('eats', 'bald_eagle', 'cow', True))
engine.add_case_fact('kb', ('eats', 'bald_eagle', 'dog', False))
engine.add_case_fact('kb', ('rough', 'bald_eagle', True))

engine.add_case_fact('kb', ('round', 'cow', True))
engine.add_case_fact('kb', ('sees', 'cow', 'bald_eagle', True))
engine.add_case_fact('kb', ('sees', 'cow', 'dog', False))
engine.add_case_fact('kb', ('visits', 'cow', 'bald_eagle', True))
engine.add_case_fact('kb', ('visits', 'cow', 'lion', True))

engine.add_case_fact('kb', ('rough', 'dog', True))

engine.add_case_fact('kb', ('young', 'lion', True))
engine.add_case_fact('kb', ('sees', 'lion', 'bald_eagle', False))
engine.add_case_fact('kb', ('sees', 'lion', 'cow', True))

# --- Rules ---
engine.add_rule('kb',
    # If someone is green and they eat the bald eagle then the bald eagle is not rough.
    (('green', '?x', True),
     ('eats', '?x', 'bald_eagle', True)),
    (('rough', 'bald_eagle', False),))

engine.add_rule('kb',
    # If someone is big and they do not see the bald eagle then the bald eagle is rough.
    (('big', '?x', True),
     ('sees', '?x', 'bald_eagle', False)),
    (('rough', 'bald_eagle', True),))

engine.add_rule('kb',
    # If someone is big then they visit the dog.
    (('big', '?x', True),),
    (('visits', '?x', 'dog', True),))

engine.add_rule('kb',
    # If someone eats the lion and they are big then the lion eats the dog.
    (('eats', '?x', 'lion', True),
     ('big', '?x', True)),
    (('eats', 'lion', 'dog', True),))

engine.add_rule('kb',
    # If someone visits the dog then the dog eats the cow.
    (('visits', '?x', 'dog', True),),
    (('eats', 'dog', 'cow', True),))

engine.add_rule('kb',
    # If someone is rough and they eat the cow then they are young.
    (('rough', '?x', True),
     ('eats', '?x', 'cow', True)),
    (('young', '?x', True),))

engine.add_rule('kb',
    # If the lion eats the cow then the lion visits the bald eagle.
    (('eats', 'lion', 'cow', True),),
    (('visits', 'lion', 'bald_eagle', True),))

engine.add_rule('kb',
    # If someone is big and they see the lion then they are green.
    (('big', '?x', True),
     ('sees', '?x', 'lion', True)),
    (('green', '?x', True),))

engine.add_rule('kb',
    # If someone is young then they are big.
    (('young', '?x', True),),
    (('big', '?x', True),))

# --- Query ---
engine.add_goal('kb', ('big', 'lion', True))