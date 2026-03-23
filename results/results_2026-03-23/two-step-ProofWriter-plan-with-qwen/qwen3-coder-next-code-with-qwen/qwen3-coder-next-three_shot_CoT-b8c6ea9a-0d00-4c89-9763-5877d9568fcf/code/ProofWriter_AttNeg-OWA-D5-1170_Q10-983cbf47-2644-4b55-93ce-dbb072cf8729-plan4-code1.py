from pyke import knowledge_engine

# Create knowledge engine instance
engine = knowledge_engine.engine(__file__)

# Load facts and rules
engine.activate('rules')

# Facts section
engine.add_fact('facts', 'is_kind', ('Bob', True))
engine.add_fact('facts', 'is_quiet', ('Charlie', True))
engine.add_fact('facts', 'is_rough', ('Charlie', True))
engine.add_fact('facts', 'is_kind', ('Fiona', True))
engine.add_fact('facts', 'is_rough', ('Fiona', True))
engine.add_fact('facts', 'is_white', ('Fiona', True))
engine.add_fact('facts', 'is_nice', ('Gary', True))

# Query section
result = engine.prove('facts', 'is_quiet', ('Gary', False), 1)
print("True" if result else "False")