# Import required modules
from pyke import knowledge_engine

# Create and initialize the knowledge engine
engine = knowledge_engine.engine(__file__)
engine.activate('rules')

# Facts
facts.is_a("Polly", "jompus", True)

# Rules (compiled into the 'rules' module)