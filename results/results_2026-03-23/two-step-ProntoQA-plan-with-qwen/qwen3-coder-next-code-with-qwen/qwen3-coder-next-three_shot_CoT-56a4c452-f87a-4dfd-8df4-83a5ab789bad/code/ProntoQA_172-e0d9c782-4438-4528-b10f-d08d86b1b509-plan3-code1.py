from pyke import knowledge_engine

# Initialize knowledge engine
engine = knowledge_engine.engine(__file__)

# Facts
engine.add_case_fact('facts', ('is_a', 'Rex', 'zumpus', True))

# Rules
@engine.rule('zumpus_is_not_temperate')
def zumpus_is_not_temperate():
    return (
        ('foreach', [('is_a', '$thing', 'zumpus', True)]),
        ('assert', [('is_temperate', '$thing', False)])
    )

@engine.rule('zumpus_is_vumpus')
def zumpus_is_vumpus():
    return (
        ('foreach', [('is_a', '$thing', 'zumpus', True)]),
        ('assert', [('is_a', '$thing', 'vumpus', True)])
    )

@engine.rule('vumpus_is_large')
def vumpus_is_large():
    return (
        ('foreach', [('is_a', '$thing', 'vumpus', True)]),
        ('assert', [('is_large', '$thing', True)])
    )

@engine.rule('vumpus_is_dumpus')
def vumpus_is_dumpus():
    return (
        ('foreach', [('is_a', '$thing', 'vumpus', True)]),
        ('assert', [('is_a', '$thing', 'dumpus', True)])
    )

@engine.rule('dumpus_is_feisty')
def dumpus_is_feisty():
    return (
        ('foreach', [('is_a', '$thing', 'dumpus', True)]),
        ('assert', [('is_feisty', '$thing', True)])
    )

@engine.rule('tumpus_is_not_opaque')
def tumpus_is_not_opaque():
    return (
        ('foreach', [('is_a', '$thing', 'tumpus', True)]),
        ('assert', [('is_opaque', '$thing', False)])
    )

@engine.rule('dumpus_is_wumpus')
def dumpus_is_wumpus():
    return (
        ('foreach', [('is_a', '$thing', 'dumpus', True)]),
        ('assert', [('is_a', '$thing', 'wumpus', True)])
    )

@engine.rule('wumpus_is_floral')
def wumpus_is_floral():
    return (
        ('foreach', [('is_a', '$thing', 'wumpus', True)]),
        ('assert', [('is_floral', '$thing', True)])
    )

@engine.rule('wumpus_is_rompus')
def wumpus_is_rompus():
    return (
        ('foreach', [('is_a', '$thing', 'wumpus', True)]),
        ('assert', [('is_a', '$thing', 'rompus', True)])
    )

@engine.rule('rompus_is_opaque')
def rompus_is_opaque():
    return (
        ('foreach', [('is_a', '$thing', 'rompus', True)]),
        ('assert', [('is_opaque', '$thing', True)])
    )

@engine.rule('rompus_is_numpus')
def rompus_is_numpus():
    return (
        ('foreach', [('is_a', '$thing', 'rompus', True)]),
        ('assert', [('is_a', '$thing', 'numpus', True)])
    )

# Activate rules and run
engine.activate('zumpus_is_not_temperate')
engine.activate('zumpus_is_vumpus')
engine.activate('vumpus_is_large')
engine.activate('vumpus_is_dumpus')
engine.activate('dumpus_is_feisty')
engine.activate('tumpus_is_not_opaque')
engine.activate('dumpus_is_wumpus')
engine.activate('wumpus_is_floral')
engine.activate('wumpus_is_rompus')
engine.activate('rompus_is_opaque')
engine.activate('rompus_is_numpus')

# Query
result = engine.query(('is_opaque', 'Rex', False))
print("Rex is not opaque:", result)