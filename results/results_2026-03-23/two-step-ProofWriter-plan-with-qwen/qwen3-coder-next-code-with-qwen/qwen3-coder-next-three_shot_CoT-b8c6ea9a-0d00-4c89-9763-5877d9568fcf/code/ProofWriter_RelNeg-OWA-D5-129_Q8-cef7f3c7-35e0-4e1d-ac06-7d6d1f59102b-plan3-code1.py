# --- Import and Setup ---
from pyke import knowledge_engine

engine = knowledge_engine.engine(__file__)

# --- Facts ---
engine.add_universal_fact('facts', 'is_cold', ('lion', True))
engine.add_universal_fact('facts', 'needs', ('lion', 'mouse'))
engine.add_universal_fact('facts', 'visits', ('lion', 'squirrel'))

engine.add_universal_fact('facts', 'is_cold', ('mouse', True))
# mouse does not visit squirrel
engine.add_universal_fact('facts', 'visits', ('mouse', 'squirrel'), False)

engine.add_universal_fact('facts', 'is_cold', ('rabbit', True))
engine.add_universal_fact('facts', 'is_rough', ('rabbit', True))
# rabbit does not need lion
engine.add_universal_fact('facts', 'needs', ('rabbit', 'lion'), False)
# rabbit does not visit squirrel
engine.add_universal_fact('facts', 'visits', ('rabbit', 'squirrel'), False)

engine.add_universal_fact('facts', 'is_kind', ('squirrel', True))
engine.add_universal_fact('facts', 'needs', ('squirrel', 'mouse'))
engine.add_universal_fact('facts', 'needs', ('squirrel', 'rabbit'))
# squirrel does not see lion
engine.add_universal_fact('facts', 'sees', ('squirrel', 'lion'), False)
# squirrel does not see rabbit
engine.add_universal_fact('facts', 'sees', ('squirrel', 'rabbit'), False)

# --- Rules ---
@engine.rule
def rule1():
    """
    If something needs the rabbit and the rabbit sees the mouse then the mouse does not see the lion.
    """
    return (
        (lambda x: engine.knowledge['facts']['needs'](x, 'rabbit') and 
                   engine.knowledge['facts']['sees']('rabbit', 'mouse'))()
    ), lambda x: engine.assert_('facts', 'sees', ('mouse', 'lion'), False)

@engine.rule
def rule2():
    """
    If something is rough then it visits the mouse.
    """
    return (
        (lambda x: engine.knowledge['facts']['is_rough'](x, True))(),
        lambda x: engine.assert_('facts', 'visits', (x, 'mouse'))
    )

@engine.rule
def rule3():
    """
    If something needs the rabbit and it visits the mouse then the mouse needs the rabbit.
    """
    return (
        (lambda x: engine.knowledge['facts']['needs'](x, 'rabbit') and 
                   engine.knowledge['facts']['visits'](x, 'mouse'))(),
        lambda x: engine.assert_('facts', 'needs', ('mouse', 'rabbit'))
    )

@engine.rule
def rule4():
    """
    If something needs the rabbit and the rabbit is cold then it is rough.
    """
    return (
        (lambda x: engine.knowledge['facts']['needs'](x, 'rabbit') and 
                   engine.knowledge['facts']['is_cold']('rabbit', True))(),
        lambda x: engine.assert_('facts', 'is_rough', (x, True))
    )

@engine.rule
def rule5():
    """
    If something needs the rabbit then the rabbit needs the squirrel.
    """
    return (
        (lambda x: engine.knowledge['facts']['needs'](x, 'rabbit'))(),
        lambda x: engine.assert_('facts', 'needs', ('rabbit', 'squirrel'))
    )

@engine.rule
def rule6():
    """
    If the squirrel sees the lion and the squirrel is not green then the lion needs the squirrel.
    """
    return (
        (lambda: engine.knowledge['facts']['sees']('squirrel', 'lion') and 
                   not engine.knowledge['facts']['is_green']('squirrel'))(),
        lambda: engine.assert_('facts', 'needs', ('lion', 'squirrel'))
    )

@engine.rule
def rule7():
    """
    If something is big then it visits the lion.
    """
    return (
        (lambda x: engine.knowledge['facts']['is_big'](x, True))(),
        lambda x: engine.assert_('facts', 'visits', (x, 'lion'))
    )

@engine.rule
def rule8():
    """
    If something visits the squirrel and the squirrel sees the lion then the lion is not kind.
    """
    return (
        (lambda x: engine.knowledge['facts']['visits'](x, 'squirrel') and 
                   engine.knowledge['facts']['sees']('squirrel', 'lion'))(),
        lambda x: engine.assert_('facts', 'is_kind', ('lion', False))
    )

# --- Query ---
engine.activate('facts')
result = engine.query('facts', 'needs', ('mouse', 'rabbit'))
print("Mouse needs rabbit:", result)

# Since we want to check "The mouse does not need the rabbit", 
# we also need to check if needs('mouse', 'rabbit') is False
try:
    # Try to prove that mouse does not need rabbit
    neg_result = engine.query('facts', 'needs', ('mouse', 'rabbit'), False)
    print("Mouse does not need rabbit:", neg_result)
except:
    # If we can't prove it's false, then it's unknown
    print("Cannot prove mouse does not need rabbit")