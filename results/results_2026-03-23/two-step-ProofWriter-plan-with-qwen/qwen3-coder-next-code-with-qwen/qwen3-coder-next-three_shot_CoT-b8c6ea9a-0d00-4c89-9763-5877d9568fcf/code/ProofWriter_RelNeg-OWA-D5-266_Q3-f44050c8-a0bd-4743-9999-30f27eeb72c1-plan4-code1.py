from pyke import knowledge_engine

# Initialize the knowledge engine
engine = knowledge_engine.engine(__file__)

# --- Facts ---
engine.add_case_fact('kb', ('eats', 'bald_eagle', 'cow'), True)
engine.add_case_fact('kb', ('eats', 'bald_eagle', 'dog'), False)
engine.add_case_fact('kb', ('is_rough', 'bald_eagle'), True)

engine.add_case_fact('kb', ('is_round', 'cow'), True)
engine.add_case_fact('kb', ('sees', 'cow', 'bald_eagle'), True)
engine.add_case_fact('kb', ('sees', 'cow', 'dog'), False)
engine.add_case_fact('kb', ('visits', 'cow', 'bald_eagle'), True)
engine.add_case_fact('kb', ('visits', 'cow', 'lion'), True)

engine.add_case_fact('kb', ('is_rough', 'dog'), True)

engine.add_case_fact('kb', ('is_young', 'lion'), True)
engine.add_case_fact('kb', ('sees', 'lion', 'bald_eagle'), False)
engine.add_case_fact('kb', ('sees', 'lion', 'cow'), True)

# --- Rules ---
@engine.rule
def rule1(kb, x):
    if kb.asserted(('is_green', x)) and kb.asserted(('eats', x, 'bald_eagle')):
        return [('is_rough', 'bald_eagle', False)]

@engine.rule
def rule2(kb, x):
    if kb.asserted(('is_big', x)) and kb.asserted(('sees', x, 'bald_eagle')):
        return [('is_rough', 'bald_eagle', True)]

@engine.rule
def rule3(kb, x):
    if kb.asserted(('is_big', x)):
        return [('visits', x, 'dog')]

@engine.rule
def rule4(kb, x):
    if kb.asserted(('eats', x, 'lion')) and kb.asserted(('is_big', x)):
        return [('eats', 'lion', 'dog')]

@engine.rule
def rule5(kb, x):
    if kb.asserted(('visits', x, 'dog')):
        return [('eats', 'dog', 'cow')]

@engine.rule
def rule6(kb, x):
    if kb.asserted(('is_rough', x)) and kb.asserted(('eats', x, 'cow')):
        return [('is_young', x)]

@engine.rule
def rule7(kb):
    if kb.asserted(('eats', 'lion', 'cow')):
        return [('visits', 'lion', 'bald_eagle')]

@engine.rule
def rule8(kb, x):
    if kb.asserted(('is_big', x)) and kb.asserted(('sees', x, 'lion')):
        return [('is_green', x)]

@engine.rule
def rule9(kb, x):
    if kb.asserted(('is_young', x)):
        return [('is_big', x)]

# --- Query ---
query_result = engine.prove_1('kb', ('is_big', 'lion'), 1)

if query_result:
    print("True")
else:
    print("False")