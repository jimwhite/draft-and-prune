# Facts:
facts = [
    ("is_a", "Fae", "numpus")
]

# Rules:
rules = [
    # Rompuses are dumpuses.
    ("rompus_is_dumpus", 
     [("is_a", "$thing", "rompus")], 
     [("is_a", "$thing", "dumpus")]),
    
    # Dumpuses are blue.
    ("dumpus_is_blue", 
     [("is_a", "$thing", "dumpus")], 
     [("is_blue", "$thing")]),
    
    # Every dumpus is a numpus.
    ("dumpus_is_numpus", 
     [("is_a", "$thing", "dumpus")], 
     [("is_a", "$thing", "numpus")]),
    
    # Every numpus is fruity.
    ("numpus_is_fruity", 
     [("is_a", "$thing", "numpus")], 
     [("is_fruity", "$thing")]),
    
    # Numpuses are jompuses.
    ("numpus_is_jompus", 
     [("is_a", "$thing", "numpus")], 
     [("is_a", "$thing", "jompus")]),
    
    # Every jompus is mean.
    ("jompus_is_mean", 
     [("is_a", "$thing", "jompus")], 
     [("is_mean", "$thing")]),
    
    # Jompuses are tumpuses.
    ("jompus_is_tumpus", 
     [("is_a", "$thing", "jompus")], 
     [("is_a", "$thing", "tumpus")]),
    
    # Tumpuses are not temperate.
    ("tumpus_is_not_temperate", 
     [("is_a", "$thing", "tumpus")], 
     [("not_temperate", "$thing")]),
    
    # Tumpuses are impuses.
    ("tumpus_is_impus", 
     [("is_a", "$thing", "tumpus")], 
     [("is_a", "$thing", "impus")]),
    
    # Impuses are not dull.
    ("impus_is_not_dull", 
     [("is_a", "$thing", "impus")], 
     [("not_dull", "$thing")]),
    
    # Each impus is a yumpus.
    ("impus_is_yumpus", 
     [("is_a", "$thing", "impus")], 
     [("is_a", "$thing", "yumpus")]),
    
    # Every yumpus is not transparent.
    ("yumpus_is_not_transparent", 
     [("is_a", "$thing", "yumpus")], 
     [("not_transparent", "$thing")]),
    
    # Yumpuses are zumpuses.
    ("yumpus_is_zumpus", 
     [("is_a", "$thing", "yumpus")], 
     [("is_a", "$thing", "zumpus")]),
    
    # Wumpuses are transparent.
    ("wumpus_is_transparent", 
     [("is_a", "$thing", "wumpus")], 
     [("transparent", "$thing")]),
    
    # Zumpuses are not sweet.
    ("zumpus_is_not_sweet", 
     [("is_a", "$thing", "zumpus")], 
     [("not_sweet", "$thing")]),
    
    # Zumpuses are vumpuses.
    ("zumpus_is_vumpus", 
     [("is_a", "$thing", "zumpus")], 
     [("is_a", "$thing", "vumpus")])
]

# Query:
query = ("transparent", "Fae")

# PyKe execution code
import pyke

def main():
    # Create knowledge engine
    ke = pyke.knowledge_engine.engine()
    
    # Add facts and rules to the engine
    for fact in facts:
        ke.add_fact(*fact)
    
    # Add rules to the engine
    for rule_name, conditions, conclusions in rules:
        ke.add_rule(rule_name, conditions, conclusions)
    
    # Run the engine to infer new facts
    ke.run()
    
    # Check if query is true
    result = ke.query(query)
    print(result)

if __name__ == "__main__":
    main()