# --- PyKe Program ---

from pyke import knowledge_engine

engine = knowledge_engine.engine(__file__)

# --- Facts ---
engine.add_rule('facts', 'is_cold', ('lion', True), ())
engine.add_rule('facts', 'needs', ('lion', 'mouse', False), ())
engine.add_rule('facts', 'visits', ('lion', 'squirrel', True), ())

engine.add_rule('facts', 'is_cold', ('mouse', True), ())
engine.add_rule('facts', 'visits', ('mouse', 'squirrel', False), ())

engine.add_rule('facts', 'is_cold', ('rabbit', True), ())
engine.add_rule('facts', 'is_rough', ('rabbit', True), ())
engine.add_rule('facts', 'needs', ('rabbit', 'lion', False), ())
engine.add_rule('facts', 'visits', ('rabbit', 'squirrel', False), ())

engine.add_rule('facts', 'is_kind', ('squirrel', True), ())
engine.add_rule('facts', 'needs', ('squirrel', 'mouse', True), ())
engine.add_rule('facts', 'needs', ('squirrel', 'rabbit', True), ())
engine.add_rule('facts', 'sees', ('squirrel', 'lion', False), ())
engine.add_rule('facts', 'sees', ('squirrel', 'rabbit', False), ())

# --- Rules ---
engine.add_rule('rules', 
    ('mouse_does_not_see_lion',),
    (('?x', 'needs', 'rabbit', True), ('sees', 'rabbit', 'mouse', True)),
    (('sees', 'mouse', 'lion', False),))

engine.add_rule('rules',
    ('rough_visits_mouse',),
    (('?x', 'is_rough', True),),
    (('?x', 'visits', 'mouse', True),))

engine.add_rule('rules',
    ('needs_rabbit_and_visits_mouse_implies_mouse_needs_rabbit',),
    (('?x', 'needs', 'rabbit', True), ('?x', 'visits', 'mouse', True)),
    (('mouse', 'needs', 'rabbit', True),))

engine.add_rule('rules',
    ('needs_rabbit_and_rabbit_cold_implies_rough',),
    (('?x', 'needs', 'rabbit', True), ('is_cold', 'rabbit', True)),
    (('?x', 'is_rough', True),))

engine.add_rule('rules',
    ('needs_rabbit_implies_rabbit_needs_squirrel',),
    (('?x', 'needs', 'rabbit', True),),
    (('rabbit', 'needs', 'squirrel', True),))

# Rule 6: squirrel sees lion and not green -> lion needs squirrel
# Since we have no information about "green", this rule won't fire.
engine.add_rule('rules',
    ('squirrel_sees_lion_and_not_green_implies_lion_needs_squirrel',),
    (('squirrel', 'sees', 'lion', True), ('not', ('is_green', 'squirrel', True))),
    (('lion', 'needs', 'squirrel', True),))

# Rule 7: big -> visits lion
engine.add_rule('rules',
    ('big_visits_lion',),
    (('?x', 'is_big', True),),
    (('?x', 'visits', 'lion', True),))

# Rule 8: visits squirrel and squirrel sees lion -> lion not kind
engine.add_rule('rules',
    ('visits_squirrel_and_squirrel_sees_lion_implies_lion_not_kind',),
    (('?x', 'visits', 'squirrel', True), ('squirrel', 'sees', 'lion', True)),
    (('is_kind', 'lion', False),))

# --- Query ---
query = engine.add_goal(('needs', 'mouse', 'rabbit', False))