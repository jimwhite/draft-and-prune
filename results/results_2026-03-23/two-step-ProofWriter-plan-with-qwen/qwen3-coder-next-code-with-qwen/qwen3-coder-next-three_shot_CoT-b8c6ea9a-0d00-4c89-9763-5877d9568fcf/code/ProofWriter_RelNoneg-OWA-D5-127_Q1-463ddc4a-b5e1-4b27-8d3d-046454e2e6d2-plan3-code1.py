from pyke import knowledge_engine, goal

# Create knowledge engine instance
engine = knowledge_engine.engine(__file__)

# Add facts
engine.add_case_fact('facts', ('is_blue', 'bear', True))
engine.add_case_fact('facts', ('is_green', 'bear', True))
engine.add_case_fact('facts', ('is_red', 'bear', True))
engine.add_case_fact('facts', ('sees', 'bear', 'rabbit', True))

engine.add_case_fact('facts', ('is_blue', 'cow', True))
engine.add_case_fact('facts', ('needs', 'cow', 'tiger', True))
engine.add_case_fact('facts', ('visits', 'cow', 'rabbit', True))

engine.add_case_fact('facts', ('is_cold', 'rabbit', True))
engine.add_case_fact('facts', ('is_nice', 'rabbit', True))
engine.add_case_fact('facts', ('needs', 'rabbit', 'cow', True))
engine.add_case_fact('facts', ('sees', 'rabbit', 'cow', True))
engine.add_case_fact('facts', ('sees', 'rabbit', 'tiger', True))

engine.add_case_fact('facts', ('needs', 'tiger', 'bear', True))
engine.add_case_fact('facts', ('needs', 'tiger', 'rabbit', True))
engine.add_case_fact('facts', ('visits', 'tiger', 'bear', True))
engine.add_case_fact('facts', ('visits', 'tiger', 'cow', True))

# Add rules
engine.add_rule('rule1',
    ( ('is_green', '?x', True), ),
    ( ('visits', '?x', 'tiger', True), ),
    ['?x']
)

engine.add_rule('rule2',
    ( ('sees', '?x', 'bear', True), ('is_cold', '?x', True) ),
    ( ('is_green', 'bear', True), )
)

engine.add_rule('rule3',
    ( ('needs', 'cow', 'rabbit', True), ('needs', 'rabbit', 'cow', True) ),
    ( ('is_red', 'rabbit', True), )
)

engine.add_rule('rule4',
    ( ('is_green', '?x', True), ),
    ( ('needs', '?x', 'cow', True), ),
    ['?x']
)

engine.add_rule('rule5',
    ( ('visits', '?x', 'tiger', True), ),
    ( ('is_red', 'tiger', True), ),
    ['?x']
)

engine.add_rule('rule6',
    ( ('needs', '?x', 'tiger', True), ('sees', 'tiger', 'cow', True) ),
    ( ('needs', 'cow', 'bear', True), ),
    ['?x']
)

engine.add_rule('rule7',
    ( ('sees', '?x', 'bear', True), ('needs', '?x', 'bear', True) ),
    ( ('sees', '?x', 'cow', True), ),
    ['?x']
)

engine.add_rule('rule8',
    ( ('visits', '?x', 'rabbit', True), ),
    ( ('needs', 'rabbit', 'tiger', True), ),
    ['?x']
)

engine.add_rule('rule9',
    ( ('needs', '?x', 'bear', True), ('visits', 'bear', 'tiger', True) ),
    ( ('sees', '?x', 'bear', True), ),
    ['?x']
)

# Add query
engine.add_goal('query', ('visits', 'cow', 'rabbit', True))

# Run the engine
engine.activate('facts')
engine.run()

# Check if query is proven
result = engine.prove('query', ('visits', 'cow', 'rabbit', True), 1)

if result:
    print("True")
else:
    print("False")