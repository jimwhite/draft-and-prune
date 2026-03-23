from pyke import knowledge_engine

engine = knowledge_engine.engine(__file__)

# Facts
engine.add_case_fact('kb', ('is_big', 'Bob', True))
engine.add_case_fact('kb', ('is_blue', 'Bob', True))
engine.add_case_fact('kb', ('is_cold', 'Bob', True))
engine.add_case_fact('kb', ('is_quiet', 'Bob', True))
engine.add_case_fact('kb', ('is_rough', 'Bob', True))
engine.add_case_fact('kb', ('is_smart', 'Bob', True))
engine.add_case_fact('kb', ('is_white', 'Bob', True))

engine.add_case_fact('kb', ('is_rough', 'Dave', True))
engine.add_case_fact('kb', ('is_blue', 'Fiona', True))
engine.add_case_fact('kb', ('is_big', 'Harry', True))
engine.add_case_fact('kb', ('is_cold', 'Harry', True))

# Rules
@engine.rule
def blue_implies_cold(kb_ctx, x):
    if kb_ctx.knowledge['is_blue'](x, True):
        return [('is_cold', x, True)]

@engine.rule
def big_implies_white(kb_ctx, x):
    if kb_ctx.knowledge['is_big'](x, True):
        return [('is_white', x, True)]

@engine.rule
def blue_and_smart_implies_big(kb_ctx, x):
    if kb_ctx.knowledge['is_blue'](x, True) and kb_ctx.knowledge['is_smart'](x, True):
        return [('is_big', x, True)]

@engine.rule
def blue_and_rough_implies_quiet(kb_ctx, x):
    if kb_ctx.knowledge['is_blue'](x, True) and kb_ctx.knowledge['is_rough'](x, True):
        return [('is_quiet', x, True)]

@engine.rule
def smart_implies_blue(kb_ctx, x):
    if kb_ctx.knowledge['is_smart'](x, True):
        return [('is_blue', x, True)]

@engine.rule
def cold_implies_rough(kb_ctx, x):
    if kb_ctx.knowledge['is_cold'](x, True):
        return [('is_rough', x, True)]

@engine.rule
def quiet_implies_big(kb_ctx, x):
    if kb_ctx.knowledge['is_quiet'](x, True):
        return [('is_big', x, True)]

# Query
result = engine.prove_1('kb', 'is_big', ('Fiona', True), None)
print("Fiona is big:", result is not None)