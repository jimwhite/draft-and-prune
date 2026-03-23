from pyke import knowledge_engine

# Create knowledge engine instance
engine = knowledge_engine.engine(__file__)

# Load the knowledge base
engine.activate('kb')

# Add facts
engine.add_case_fact('kb', ('is_a', 'Sam', 'numpus', True))

# Run inference
engine.run()

# Query the result: Is Sam NOT dull?
result = engine.query('kb', 'is_dull', ('Sam', False), None)

# Print result
print(result)