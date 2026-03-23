from pyke import knowledge_engine

engine = knowledge_engine.engine(__file__)

# Facts
engine.add_predicate('is_blue', 'Anne', True)
engine.add_predicate('is_cold', 'Anne', True)
engine.add_predicate('is_kind', 'Anne', True)
engine.add_predicate('is_quiet', 'Anne', True)

engine.add_predicate('is_blue', 'Bob', True)
engine.add_predicate('is_kind', 'Bob', True)
engine.add_predicate('is_nice', 'Bob', True)
engine.add_predicate('is_not_quiet', 'Bob', True)

engine.add_predicate('is_not_furry', 'Dave', True)
engine.add_predicate('is_green', 'Dave', True)
engine.add_predicate('is_quiet', 'Dave', True)

engine.add_predicate('is_cold', 'Fiona', True)

# Rules
@engine.rule
def cold_people_are_blue(x):
    return (
        ('is_cold', x, True),
        '=>',
        ('is_blue', x, True)
    )

@engine.rule
def green_nice_people_are_kind(x):
    return (
        ('is_green', x, True),
        ('is_nice', x, True),
        '=>',
        ('is_kind', x, True)
    )

@engine.rule
def blue_people_are_kind(x):
    return (
        ('is_blue', x, True),
        '=>',
        ('is_kind', x, True)
    )

@engine.rule
def kind_cold_people_are_nice(x):
    return (
        ('is_kind', x, True),
        ('is_cold', x, True),
        '=>',
        ('is_nice', x, True)
    )

@engine.rule
def nice_people_are_green(x):
    return (
        ('is_nice', x, True),
        '=>',
        ('is_green', x, True)
    )

@engine.rule
def cold_green_people_are_quiet(x):
    return (
        ('is_cold', x, True),
        ('is_green', x, True),
        '=>',
        ('is_quiet', x, True)
    )

# Query
result = engine.query(('is_kind', 'Fiona', False))
print(result)