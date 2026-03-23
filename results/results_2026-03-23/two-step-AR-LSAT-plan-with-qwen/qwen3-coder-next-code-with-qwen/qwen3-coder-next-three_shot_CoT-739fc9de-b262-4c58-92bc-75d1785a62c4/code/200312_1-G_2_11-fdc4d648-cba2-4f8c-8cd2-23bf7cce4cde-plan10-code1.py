from z3 import *

# Cargo type indices: 0-fuel, 1-grain, 2-livestock, 3-machinery, 4-produce, 5-textiles
pos = {
    'fuel': Int('pos_fuel'),
    'grain': Int('pos_grain'),
    'livestock': Int('pos_livestock'),
    'machinery': Int('pos_machinery'),
    'produce': Int('pos_produce'),
    'textiles': Int('pos_textiles')
}

# Base solver
solver = Solver()

# Domain constraints: positions 1-6, all distinct
for v in pos.values():
    solver.add(v >= 1, v <= 6)
solver.add(Distinct(*pos.values()))

# Base ordering constraints
solver.add(pos['grain'] > pos['livestock'])
solver.add(pos['livestock'] > pos['textiles'])
solver.add(pos['produce'] > pos['fuel'])

# Adjacency constraint: textiles next to produce
solver.add(Or(
    pos['textiles'] == pos['produce'] + 1,
    pos['textiles'] == pos['produce'] - 1
))

# Scenario-specific constraint: produce next to livestock
solver.add(Or(
    pos['produce'] == pos['livestock'] + 1,
    pos['produce'] == pos['livestock'] - 1
))

# Answer choices: each is a constraint to test
answer_choices = [
    pos['fuel'] == 2,           # Bay 2 is holding fuel
    pos['produce'] == 4,        # Bay 4 is holding produce
    pos['textiles'] == 4,       # Bay 4 is holding textiles
    pos['grain'] == 5,          # Bay 5 is holding grain
    pos['machinery'] == 5       # Bay 5 is holding machinery
]

# Check each answer choice under the scenario
answer_index_list = []
for idx, constraint in enumerate(answer_choices):
    s_chk = Solver()
    # Add all base + scenario constraints
    for a in solver.assertions():
        s_chk.add(a)
    # Add the specific answer choice constraint
    s_chk.add(constraint)
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)