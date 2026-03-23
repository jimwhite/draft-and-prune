from z3 import *

# Cargo type indices
(FUEL, GRAIN, LIVESTOCK, MACHINERY, PRODUCE, TEXTILES) = range(6)

# pos[type] = position (1-6) of the cargo type
pos = {t: Int(f"pos_{t}") for t in [FUEL, GRAIN, LIVESTOCK, MACHINERY, PRODUCE, TEXTILES]}

# Base solver for the conditional scenario
solver = Solver()

# Domain constraints: positions 1-6, all distinct
for t in pos:
    solver.add(pos[t] >= 1, pos[t] <= 6)
solver.add(Distinct(*pos.values()))

# Baseline constraints (always true)
solver.add(pos[GRAIN] > pos[LIVESTOCK])
solver.add(pos[LIVESTOCK] > pos[TEXTILES])
solver.add(pos[PRODUCE] > pos[FUEL])
# Textiles and produce are adjacent
solver.add(Or(pos[TEXTILES] == pos[PRODUCE] + 1, pos[TEXTILES] == pos[PRODUCE] - 1))

# Conditional constraint: produce is next to livestock
solver.add(Or(pos[PRODUCE] == pos[LIVESTOCK] + 1, pos[PRODUCE] == pos[LIVESTOCK] - 1))

# Answer choices: list of (description, constraint)
answer_choices = [
    ("Bay 2 is holding fuel.", pos[FUEL] == 2),
    ("Bay 4 is holding produce.", pos[PRODUCE] == 4),
    ("Bay 4 is holding textiles.", pos[TEXTILES] == 4),
    ("Bay 5 is holding grain.", pos[GRAIN] == 5),
    ("Bay 5 is holding machinery.", pos[MACHINERY] == 5)
]

# Check each answer choice
answer_index_list = []
for idx, (_, constraint) in enumerate(answer_choices):
    s_chk = Solver()
    # Add all baseline and conditional constraints
    for assertion in solver.assertions():
        s_chk.add(assertion)
    # Add the specific choice constraint
    s_chk.add(constraint)
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)