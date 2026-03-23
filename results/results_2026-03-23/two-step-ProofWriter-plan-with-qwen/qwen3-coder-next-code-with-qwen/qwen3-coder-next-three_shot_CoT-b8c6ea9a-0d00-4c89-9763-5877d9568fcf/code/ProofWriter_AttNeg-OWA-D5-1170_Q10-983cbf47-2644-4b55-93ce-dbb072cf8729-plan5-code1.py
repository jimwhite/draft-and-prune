from pyke import knowledge_engine, goal

# Initialize the knowledge engine
engine = knowledge_engine.engine(__file__)

# Add facts to the knowledge base
engine.add_predicate('is_kind', 2)
engine.add_predicate('is_quiet', 2)
engine.add_predicate('is_rough', 2)
engine.add_predicate('is_white', 2)
engine.add_predicate('is_red', 2)
engine.add_predicate('is_nice', 2)
engine.add_predicate('is_smart', 2)

# Add facts
engine.add_fact('is_kind', 'Bob', True)
engine.add_fact('is_quiet', 'Charlie', True)
engine.add_fact('is_rough', 'Charlie', True)
engine.add_fact('is_kind', 'Fiona', True)
engine.add_fact('is_rough', 'Fiona', True)
engine.add_fact('is_white', 'Fiona', True)
engine.add_fact('is_nice', 'Gary', True)

# Add rules
# If Gary is red and Gary is white then Gary is quiet.
engine.add_rule(
    ('is_red', '?x', True),
    ('is_white', '?x', True),
    lambda: engine.add_fact('is_quiet', '?x', True)
)

# All white things are rough.
engine.add_rule(
    ('is_white', '?x', True),
    lambda: engine.add_fact('is_rough', '?x', True)
)

# If something is rough then it is red.
engine.add_rule(
    ('is_rough', '?x', True),
    lambda: engine.add_fact('is_red', '?x', True)
)

# If something is nice then it is white.
engine.add_rule(
    ('is_nice', '?x', True),
    lambda: engine.add_fact('is_white', '?x', True)
)

# All smart things are white.
engine.add_rule(
    ('is_smart', '?x', True),
    lambda: engine.add_fact('is_white', '?x', True)
)

# Rough, quiet things are not kind.
engine.add_rule(
    ('is_rough', '?x', True),
    ('is_quiet', '?x', True),
    lambda: engine.add_fact('is_kind', '?x', False)
)

# If something is quiet and not smart then it is kind.
engine.add_rule(
    ('is_quiet', '?x', True),
    lambda: not engine.has_fact('is_smart', '?x', True),
    lambda: engine.add_fact('is_kind', '?x', True)
)

# Smart things are quiet.
engine.add_rule(
    ('is_smart', '?x', True),
    lambda: engine.add_fact('is_quiet', '?x', True)
)

# If something is smart and not rough then it is quiet.
engine.add_rule(
    ('is_smart', '?x', True),
    lambda: not engine.has_fact('is_rough', '?x', True),
    lambda: engine.add_fact('is_quiet', '?x', True)
)

# Query: is Gary not quiet? (i.e., is_quiet("Gary", False))
result = engine.query(('is_quiet', 'Gary', False))

# Output the result
if result:
    print("True")
else:
    # Try to prove the negation by checking if we can derive is_quiet("Gary", True)
    result_positive = engine.query(('is_quiet', 'Gary', True))
    if result_positive:
        print("False")
    else:
        print("Unknown")