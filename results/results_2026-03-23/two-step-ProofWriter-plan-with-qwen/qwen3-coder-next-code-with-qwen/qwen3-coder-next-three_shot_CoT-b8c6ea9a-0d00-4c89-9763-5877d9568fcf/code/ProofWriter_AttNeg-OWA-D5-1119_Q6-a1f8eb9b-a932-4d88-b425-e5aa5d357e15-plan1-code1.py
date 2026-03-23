from pyke import knowledge_engine, goal

# Initialize knowledge engine
engine = knowledge_engine.engine(__file__)

# Define facts
def add_facts():
    # Anne's properties
    engine.add_fact('facts', 'is_blue', ('Anne', True))
    engine.add_fact('facts', 'is_cold', ('Anne', True))
    engine.add_fact('facts', 'is_kind', ('Anne', True))
    engine.add_fact('facts', 'is_quiet', ('Anne', True))
    
    # Bob's properties
    engine.add_fact('facts', 'is_blue', ('Bob', True))
    engine.add_fact('facts', 'is_kind', ('Bob', True))
    engine.add_fact('facts', 'is_nice', ('Bob', True))
    engine.add_fact('facts', 'is_quiet', ('Bob', False))
    
    # Dave's properties
    engine.add_fact('facts', 'is_furry', ('Dave', False))
    engine.add_fact('facts', 'is_green', ('Dave', True))
    engine.add_fact('facts', 'is_quiet', ('Dave', True))
    
    # Fiona's properties
    engine.add_fact('facts', 'is_cold', ('Fiona', True))

# Define rules
@engine.rule('rules')
def cold_to_blue():
    return (
        ('facts', 'is_cold', ('?x', True)),
        (),
        [('facts', 'is_blue', ('?x', True))]
    )

@engine.rule('rules')
def green_and_nice_to_kind():
    return (
        ('facts', 'is_green', ('?x', True)),
        ('facts', 'is_nice', ('?x', True)),
        [('facts', 'is_kind', ('?x', True))]
    )

@engine.rule('rules')
def blue_to_kind():
    return (
        ('facts', 'is_blue', ('?x', True)),
        (),
        [('facts', 'is_kind', ('?x', True))]
    )

@engine.rule('rules')
def kind_and_cold_to_nice():
    return (
        ('facts', 'is_kind', ('?x', True)),
        ('facts', 'is_cold', ('?x', True)),
        [('facts', 'is_nice', ('?x', True))]
    )

@engine.rule('rules')
def nice_to_green():
    return (
        ('facts', 'is_nice', ('?x', True)),
        (),
        [('facts', 'is_green', ('?x', True))]
    )

@engine.rule('rules')
def cold_and_green_to_quiet():
    return (
        ('facts', 'is_cold', ('?x', True)),
        ('facts', 'is_green', ('?x', True)),
        [('facts', 'is_quiet', ('?x', True))]
    )

# Main execution
if __name__ == "__main__":
    # Add facts and rules to engine
    add_facts()
    
    # Enable the rules (activate rulebases)
    engine.activate('rules')
    
    # Query: is Fiona not kind?
    try:
        result = list(engine.prove('facts', 'is_kind', ('Fiona', True), 1))
        if result:
            print("False")  # Fiona IS kind, so "Fiona is not kind" is false
        else:
            # Try to prove she's not kind directly
            result_not = list(engine.prove('facts', 'is_kind', ('Fiona', False), 1))
            if result_not:
                print("True")  # Fiona is not kind
            else:
                print("Unknown")
    except Exception as e:
        # If we can't determine, it's unknown
        print("Unknown")