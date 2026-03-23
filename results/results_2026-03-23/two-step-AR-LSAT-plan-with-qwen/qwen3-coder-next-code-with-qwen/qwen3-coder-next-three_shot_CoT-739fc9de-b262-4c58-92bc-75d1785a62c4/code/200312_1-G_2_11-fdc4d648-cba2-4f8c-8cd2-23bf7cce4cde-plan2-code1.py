from z3 import *

# Cargo type indices: fuel, grain, livestock, machinery, produce, textiles
(FUEL, GRAIN, LIVESTOCK, MACHINERY, PRODUCE, TEXTILES) = range(6)

# Position variables: pos[type] = bay number (1-6)
pos = {t: Int(f"pos_{t}") for t in [FUEL, GRAIN, LIVESTOCK, MACHINERY, PRODUCE, TEXTILES]}

# Base solver
solver = Solver()

# Domain constraints: each position between 1 and 6, all distinct
for t in pos:
    solver.add(pos[t] >= 1, pos[t] <= 6)
solver.add(Distinct(*pos.values()))

# Given ordering constraints
solver.add(pos[GRAIN] > pos[LIVESTOCK])
solver.add(pos[LIVESTOCK] > pos[TEXTILES])
solver.add(pos[PRODUCE] > pos[FUEL])
solver.add(Or(pos[TEXTILES] == pos[PRODUCE] + 1, pos[TEXTILES] == pos[PRODUCE] - 1))

# Hypothetical condition: produce is next to livestock
solver.add(Or(pos[PRODUCE] == pos[LIVESTOCK] + 1, pos[PRODUCE] == pos[LIVESTOCK] - 1))

# Answer choices predicates
answer_predicates = [
    pos[FUEL] == 2,      # A: Bay 2 is holding fuel
    pos[PRODUCE] == 4,   # B: Bay 4 is holding produce
    pos[TEXTILES] == 4,  # C: Bay 4 is holding textiles
    pos[GRAIN] == 5,     # D: Bay 5 is holding grain
    pos[MACHINERY] == 5  # E: Bay 5 is holding machinery
]

# Check each answer choice
answer_index_list = []
for idx, pred in enumerate(answer_predicates):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(pred)
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)