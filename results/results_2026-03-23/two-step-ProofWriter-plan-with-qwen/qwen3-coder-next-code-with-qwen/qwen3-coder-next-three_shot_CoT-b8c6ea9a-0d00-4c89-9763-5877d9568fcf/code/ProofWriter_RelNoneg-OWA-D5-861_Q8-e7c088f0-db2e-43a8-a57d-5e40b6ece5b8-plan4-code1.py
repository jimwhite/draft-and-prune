from pyke import knowledge_engine, facts, rules

# Create knowledge engine instance
engine = knowledge_engine.engine(__name__)

# --- Facts ---
engine.add_case_fact('domain', 'needs', ('cat', 'dog'))
engine.add_case_fact('domain', 'is_kind', ('dog',))
engine.add_case_fact('domain', 'needs', ('dog', 'rabbit'))
engine.add_case_fact('domain', 'eats', ('rabbit', 'dog'))
engine.add_case_fact('domain', 'is_green', ('rabbit',))
engine.add_case_fact('domain', 'chases', ('tiger', 'rabbit'))
engine.add_case_fact('domain', 'is_big', ('tiger',))

# --- Rules ---
@rules.rule(
    '$x is nice and $x eats the tiger',
    'domain',
    ['nice($x)', 'eats($x, "tiger")'],
    'domain',
    ['needs($x, "dog")']
)
def rule1():
    pass

@rules.rule(
    '$x chases the cat',
    'domain',
    ['chases($x, "cat")'],
    'domain',
    ['eats($x, "cat")']
)
def rule2():
    pass

@rules.rule(
    'dog chases the tiger',
    'domain',
    ['chases("dog", "tiger")'],
    'domain',
    ['needs("tiger", "rabbit")']
)
def rule3():
    pass

@rules.rule(
    'rabbit chases the tiger',
    'domain',
    ['chases("rabbit", "tiger")'],
    'domain',
    ['chases("rabbit", "cat")']
)
def rule4():
    pass

@rules.rule(
    '$x chases the cat',
    'domain',
    ['chases($x, "cat")'],
    'domain',
    ['is_kind("cat",)']
)
def rule5():
    pass

@rules.rule(
    '$x eats the dog',
    'domain',
    ['eats($x, "dog")'],
    'domain',
    ['chases($x, "cat")']
)
def rule6():
    pass

@rules.rule(
    '$x is rough',
    'domain',
    ['is_rough($x)'],
    'domain',
    ['eats($x, "dog")']
)
def rule7():
    pass

@rules.rule(
    '$x is kind',
    'domain',
    ['is_kind($x)'],
    'domain',
    ['is_rough($x)']
)
def rule8():
    pass

@rules.rule(
    '$x eats the rabbit and rabbit is big',
    'domain',
    ['eats($x, "rabbit")', 'is_big("rabbit",)'],
    'domain',
    ['is_kind($x,)']
)
def rule9():
    pass

# --- Query ---
# We want to check if "the cat is not rough", i.e., is_rough("cat") is false
# In PyKe, we can check this by trying to prove is_rough("cat") and seeing if it fails
# The query should be: not(is_rough("cat"))
query_result = engine.prove('domain', 'is_rough', ('cat',), 1)

# Since we want to know if "the cat is not rough", we check if the proof fails
# If query_result is None (proof fails), then cat is not rough -> True
# If query_result is not None, then cat is rough -> False

print("cat is rough?" if query_result else "cat is not rough")