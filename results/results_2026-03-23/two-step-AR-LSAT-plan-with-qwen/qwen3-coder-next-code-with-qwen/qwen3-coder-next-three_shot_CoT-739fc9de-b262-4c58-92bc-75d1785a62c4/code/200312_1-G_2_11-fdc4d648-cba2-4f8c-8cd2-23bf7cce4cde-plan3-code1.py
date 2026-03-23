from z3 import *

# Cargo type indices: 0=fuel, 1=grain, 2=livestock, 3=machinery, 4=produce, 5=textiles
(FUEL, GRAIN, LIVESTOCK, MACHINERY, PRODUCE, TEXTILES) = range(6)

# Position variables: pos[type] = bay number (1-6)
pos = {t: Int(f"pos_{t}") for t in range(6)}

# Base solver
solver = Solver()

# Domain constraints: positions between 1 and 6, all distinct
for t in range(6):
    solver.add(pos[t] >= 1, pos[t] <= 6)
solver.add(Distinct(*[pos[t] for t in range(6)]))

# Base ordering constraints
solver.add(pos[GRAIN] > pos[LIVESTOCK])
solver.add(pos[LIVESTOCK] > pos[TEXTILES])
solver.add(pos[PRODUCE] > pos[FUEL])

# Textiles adjacent to produce
solver.add(Or(pos[TEXTILES] == pos[PRODUCE] + 1, pos[TEXTILES] == pos[PRODUCE] - 1))

# Conditional constraint: produce adjacent to livestock
solver.add(Or(pos[PRODUCE] == pos[LIVESTOCK] + 1, pos[PRODUCE] == pos[LIVESTOCK] - 1))

# Answer choices conditions
answer_conditions = [
    pos[FUEL] == 2,           # Bay 2 is holding fuel
    pos[PRODUCE] == 4,        # Bay 4 is holding produce
    pos[TEXTILES] == 4,       # Bay 4 is holding textiles
    pos[GRAIN] == 5,          # Bay 5 is holding grain
    pos[MACHINERY] == 5       # Bay 5 is holding machinery
]

# Check each answer choice
answer_index_list = []
for idx, cond in enumerate(answer_conditions):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(cond)
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

# Output the EXCEPT answer (the first one in the list since there should be exactly one)
print(answer_index_list[0])