# Import required modules
from pyke import knowledge_engine

# Create knowledge engine instance
engine = knowledge_engine.engine(__file__)

# Define facts
engine.add_predicate('is_blue', 'Anne', True)
engine.add_predicate('is_cold', 'Anne', True)
engine.add_predicate('is_kind', 'Anne', True)
engine.add_predicate('is_quiet', 'Anne', True)

engine.add_predicate('is_blue', 'Bob', True)
engine.add_predicate('is_kind', 'Bob', True)
engine.add_predicate('is_nice', 'Bob', True)
engine.add_predicate('is_quiet', 'Bob', False)

engine.add_predicate('is_furry', 'Dave', False)
engine.add_predicate('is_green', 'Dave', True)
engine.add_predicate('is_quiet', 'Dave', True)

engine.add_predicate('is_cold', 'Fiona', True)

# Define rules
@engine.rule
def cold_implies_blue(x):
    return (
        ('is_cold', x, True),
        '=>',
        ('is_blue', x, True)
    )

@engine.rule
def green_and_nice_implies_kind(x):
    return (
        ('is_green', x, True),
        ('is_nice', x, True),
        '=>',
        ('is_kind', x, True)
    )

@engine.rule
def blue_implies_kind(x):
    return (
        ('is_blue', x, True),
        '=>',
        ('is_kind', x, True)
    )

@engine.rule
def kind_and_cold_implies_nice(x):
    return (
        ('is_kind', x, True),
        ('is_cold', x, True),
        '=>',
        ('is_nice', x, True)
    )

@engine.rule
def nice_implies_green(x):
    return (
        ('is_nice', x, True),
        '=>',
        ('is_green', x, True)
    )

@engine.rule
def cold_and_green_implies_quiet(x):
    return (
        ('is_cold', x, True),
        ('is_green', x, True),
        '=>',
        ('is_quiet', x, True)
    )

# Add facts to engine
engine.activate('facts')

# Query: is Fiona not kind?
result = engine.query(('is_kind', 'Fiona', True))
print("Fiona is kind:", result)

# Since we want to check if "Fiona is not kind" is true
fiona_not_kind = not result
print("Fiona is not kind:", fiona_not_kind)