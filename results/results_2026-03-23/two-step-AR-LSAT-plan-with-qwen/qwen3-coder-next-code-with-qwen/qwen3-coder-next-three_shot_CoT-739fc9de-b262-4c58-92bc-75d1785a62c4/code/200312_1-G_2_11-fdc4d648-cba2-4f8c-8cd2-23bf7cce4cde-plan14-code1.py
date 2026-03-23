from z3 import *

# Cargo type indices: 0-fuel, 1-grain, 2-livestock, 3-machinery, 4-produce, 5-textiles
(FUEL, GRAIN, LIVESTOCK, MACHINERY, PRODUCE, TEXTILES) = range(6)

# Position variables: pos[type] = bay number (1-6)
pos = {t: Int(f"pos_{t}") for t in [FUEL, GRAIN, LIVESTOCK, MACHINERY, PRODUCE, TEXTILES]}

# Base solver
solver = Solver()

# Domain constraints: positions in [1,6] and all distinct
for t in pos:
    solver.add(pos[t] >= 1, pos[t] <= 6)
solver.add(Distinct(*pos.values()))

# Base ordering constraints
solver.add(pos[GRAIN] > pos[LIVESTOCK])
solver.add(pos[LIVESTOCK] > pos[TEXTILES])
solver.add(pos[PRODUCE] > pos[FUEL])
# Textiles adjacent to produce
solver.add(Or(pos[TEXTILES] == pos[PRODUCE] + 1, pos[TEXTILES] == pos[PRODUCE] - 1))

# Hypothetical constraint: produce is next to livestock
solver.add(Or(pos[PRODUCE] == pos[LIVESTOCK] + 1, pos[PRODUCE] == pos[LIVESTOCK] - 1))

# Answer choices: translate to constraints
answer_choices = [
    (FUEL, 2),   # Bay 2 is holding fuel
    (PRODUCE, 4), # Bay 4 is holding produce
    (TEXTILES, 4), # Bay 4 is holding textiles
    (GRAIN, 5),   # Bay 5 is holding grain
    (MACHINERY, 5) # Bay 5 is holding machinery
]

# Check each answer choice
answer_index_list = []
for idx, (cargo_type, bay_num) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add constraint for the specific bay assignment
    s_chk.add(pos[cargo_type] == bay_num)
    
    # If UNSAT, this choice cannot be true (EXCEPT candidate)
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)