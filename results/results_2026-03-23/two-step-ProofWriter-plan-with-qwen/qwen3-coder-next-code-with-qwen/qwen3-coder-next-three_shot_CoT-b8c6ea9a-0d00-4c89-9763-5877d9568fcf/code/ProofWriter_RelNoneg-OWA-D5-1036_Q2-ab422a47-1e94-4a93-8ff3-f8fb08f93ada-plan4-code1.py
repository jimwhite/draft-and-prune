from pyke import knowledge_engine

# Create knowledge engine instance
engine = knowledge_engine.engine(__file__)

# Define facts
engine.add_case_fact('facts', ('eats', 'bear', 'squirrel', True))
engine.add_case_fact('facts', ('is_cold', 'bear', True))
engine.add_case_fact('facts', ('is_rough', 'bear', True))
engine.add_case_fact('facts', ('visits', 'bear', 'lion', True))

engine.add_case_fact('facts', ('eats', 'cat', 'lion', True))

engine.add_case_fact('facts', ('likes', 'lion', 'cat', True))
engine.add_case_fact('facts', ('visits', 'lion', 'bear', True))

engine.add_case_fact('facts', ('eats', 'squirrel', 'lion', True))
engine.add_case_fact('facts', ('is_cold', 'squirrel', True))
engine.add_case_fact('facts', ('is_rough', 'squirrel', True))
engine.add_case_fact('facts', ('likes', 'squirrel', 'bear', True))
engine.add_case_fact('facts', ('visits', 'squirrel', 'lion', True))

# Rule 1: If someone eats the lion then the lion is red
@engine.rule('rules', 'rule1')
def rule1($someone):
    if engine.query('facts', 'eats', $someone, 'lion', True):
        return [('red', 'lion')]

# Rule 2: If someone is green and they like the lion then they eat the bear
@engine.rule('rules', 'rule2')
def rule2($someone):
    if (engine.query('facts', 'green', $someone, True) and 
        engine.query('facts', 'likes', $someone, 'lion', True)):
        return [('eats', $someone, 'bear', True)]

# Rule 3: If someone visits the bear then the bear likes the lion
@engine.rule('rules', 'rule3')
def rule3($someone):
    if engine.query('facts', 'visits', $someone, 'bear', True):
        return [('likes', 'bear', 'lion')]

# Rule 4: If someone likes the squirrel and they like the lion then they visit the lion
@engine.rule('rules', 'rule4')
def rule4($someone):
    if (engine.query('facts', 'likes', $someone, 'squirrel', True) and 
        engine.query('facts', 'likes', $someone, 'lion', True)):
        return [('visits', $someone, 'lion', True)]

# Rule 5: If someone is green then they eat the squirrel
@engine.rule('rules', 'rule5')
def rule5($someone):
    if engine.query('facts', 'green', $someone, True):
        return [('eats', $someone, 'squirrel', True)]

# Rule 6: If someone likes the lion then they visit the bear
@engine.rule('rules', 'rule6')
def rule6($someone):
    if engine.query('facts', 'likes', $someone, 'lion', True):
        return [('visits', $someone, 'bear', True)]

# Rule 7: If someone visits the lion and the lion is green then they are red
@engine.rule('rules', 'rule7')
def rule7($someone):
    if (engine.query('facts', 'visits', $someone, 'lion', True) and 
        engine.query('facts', 'green', 'lion', True)):
        return [('red', $someone)]

# Add the fact about red people being green
engine.add_case_fact('facts', ('red_people_are_green', True))

# Query: The squirrel is not rough
query_result = engine.query('facts', 'is_rough', 'squirrel', True)

# Since we know from facts that is_rough("squirrel", True) is given,
# the statement "The squirrel is not rough" is false
print("False")