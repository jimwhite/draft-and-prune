from pyke import knowledge_engine

engine = knowledge_engine.engine(__file__)

# Facts
engine.add_predicate('is_young', 'Charlie', True)
engine.add_predicate('is_blue', 'Erin', True)
engine.add_predicate('is_kind', 'Erin', False)  # Erin is not kind
engine.add_predicate('is_blue', 'Fiona', True)
engine.add_predicate('is_white', 'Fiona', True)
engine.add_predicate('is_blue', 'Gary', True)
engine.add_predicate('is_kind', 'Gary', True)

# Rules
@engine.rule
def young_and_blue_to_smart($x):
    if engine.query('is_young', $x, True) and engine.query('is_blue', $x, True):
        return [('is_smart', $x, True)]

@engine.rule
def blue_and_smart_to_furry($x):
    if engine.query('is_blue', $x, True) and engine.query('is_smart', $x, True):
        return [('is_furry', $x, True)]

@engine.rule
def smart_and_white_to_furry($x):
    if engine.query('is_smart', $x, True) and engine.query('is_white', $x, True):
        return [('is_furry', $x, True)]

@engine.rule
def young_to_nice($x):
    if engine.query('is_young', $x, True):
        return [('is_nice', $x, True)]

@engine.rule
def nice_to_blue($x):
    if engine.query('is_nice', $x, True):
        return [('is_blue', $x, True)]

@engine.rule
def furry_and_nice_to_white($x):
    if engine.query('is_furry', $x, True) and engine.query('is_nice', $x, True):
        return [('is_white', $x, True)]

# Special cases
@engine.rule
def fiona_smart_and_young_to_not_furry():
    if engine.query('is_smart', 'Fiona', True) and engine.query('is_young', 'Fiona', True):
        return [('is_furry', 'Fiona', False)]

@engine.rule
def erin_kind_to_furry():
    if engine.query('is_kind', 'Erin', True):
        return [('is_furry', 'Erin', True)]

@engine.rule
def gary_smart_and_white_to_not_kind():
    if engine.query('is_smart', 'Gary', True) and engine.query('is_white', 'Gary', True):
        return [('is_kind', 'Gary', False)]

# Query
result = engine.query('is_white', 'Fiona', False)
print(result)