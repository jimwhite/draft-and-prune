from pyke import knowledge_engine, goal

# Create knowledge engine instance
engine = knowledge_engine.engine(__file__)

# --- Facts ---
def add_facts():
    # Bear facts
    engine.add_case_fact('facts', ('is_blue', 'bear', True))
    engine.add_case_fact('facts', ('is_green', 'bear', True))
    engine.add_case_fact('facts', ('is_red', 'bear', True))
    engine.add_case_fact('facts', ('sees', 'bear', 'rabbit', True))

    # Cow facts
    engine.add_case_fact('facts', ('is_blue', 'cow', True))
    engine.add_case_fact('facts', ('needs', 'cow', 'tiger', True))
    engine.add_case_fact('facts', ('visits', 'cow', 'rabbit', True))

    # Rabbit facts
    engine.add_case_fact('facts', ('is_cold', 'rabbit', True))
    engine.add_case_fact('facts', ('is_nice', 'rabbit', True))
    engine.add_case_fact('facts', ('needs', 'rabbit', 'cow', True))
    engine.add_case_fact('facts', ('sees', 'rabbit', 'cow', True))
    engine.add_case_fact('facts', ('sees', 'rabbit', 'tiger', True))

    # Tiger facts
    engine.add_case_fact('facts', ('needs', 'tiger', 'bear', True))
    engine.add_case_fact('facts', ('needs', 'tiger', 'rabbit', True))
    engine.add_case_fact('facts', ('visits', 'tiger', 'bear', True))
    engine.add_case_fact('facts', ('visits', 'tiger', 'cow', True))

# --- Rules ---
def add_rules():
    # Rule 1: If something is green then it visits the tiger
    engine.add_rule('rules', '''
        foreach facts.is_green(?x)
        assert facts.visits(?x, "tiger", True)
    ''')

    # Rule 2: If something sees the bear and it is cold then the bear is green
    engine.add_rule('rules', '''
        foreach facts.sees(?x, "bear") and facts.is_cold(?x)
        assert facts.is_green("bear", True)
    ''')

    # Rule 3: If the cow needs the rabbit and the rabbit needs the cow then the rabbit is red
    engine.add_rule('rules', '''
        foreach facts.needs("cow", "rabbit") and facts.needs("rabbit", "cow")
        assert facts.is_red("rabbit", True)
    ''')

    # Rule 4: If something is green then it needs the cow
    engine.add_rule('rules', '''
        foreach facts.is_green(?x)
        assert facts.needs(?x, "cow", True)
    ''')

    # Rule 5: If something visits the tiger then the tiger is red
    engine.add_rule('rules', '''
        foreach facts.visits(?x, "tiger")
        assert facts.is_red("tiger", True)
    ''')

    # Rule 6: If something needs the tiger and the tiger sees the cow then the cow needs the bear
    engine.add_rule('rules', '''
        foreach facts.needs(?x, "tiger") and facts.sees("tiger", "cow")
        assert facts.needs("cow", "bear", True)
    ''')

    # Rule 7: If something sees the bear and it needs the bear then it sees the cow
    engine.add_rule('rules', '''
        foreach facts.sees(?x, "bear") and facts.needs(?x, "bear")
        assert facts.sees(?x, "cow", True)
    ''')

    # Rule 8: If something visits the rabbit then the rabbit needs the tiger
    engine.add_rule('rules', '''
        foreach facts.visits(?x, "rabbit")
        assert facts.needs("rabbit", "tiger", True)
    ''')

    # Rule 9: If something needs the bear and the bear visits the tiger then it sees the bear
    engine.add_rule('rules', '''
        foreach facts.needs(?x, "bear") and facts.visits("bear", "tiger")
        assert facts.sees(?x, "bear", True)
    ''')

# --- Main execution ---
def main():
    # Add facts and rules
    add_facts()
    add_rules()
    
    # Activate the knowledge base
    engine.activate('rules')
    
    # Query: does the cow visit the rabbit?
    try:
        result = engine.prove('facts', 'visits', ('cow', 'rabbit', True), 1)
        if result:
            print("True")
        else:
            print("False")
    except Exception as e:
        # If we can't prove it, check if it's explicitly stated or inferred
        # Since visits("cow", "rabbit", True) is a fact, it should be true
        print("Unknown")

if __name__ == "__main__":
    main()