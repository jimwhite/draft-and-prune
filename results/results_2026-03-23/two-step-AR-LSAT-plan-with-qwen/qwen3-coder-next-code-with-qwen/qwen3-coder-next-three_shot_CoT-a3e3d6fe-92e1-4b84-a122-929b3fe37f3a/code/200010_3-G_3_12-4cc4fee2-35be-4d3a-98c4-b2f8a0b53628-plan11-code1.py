from z3 import *

# Compositions indices: F=0, H=1, L=2, O=3, P=4, R=5, S=6, T=7
compositions = ["F", "H", "L", "O", "P", "R", "S", "T"]
comp_idx = {c: i for i, c in enumerate(compositions)}

# Position variables
pos = [Int(f"pos_{c}") for c in compositions]

# Base solver
solver = Solver()

# Domain constraints: positions 1-8 and all different
for i in range(8):
    solver.add(pos[i] >= 1, pos[i] <= 8)
solver.add(Distinct(*pos))

# T-F-R adjacency constraint: either T immediately before F OR T immediately after R
solver.add(Or(
    pos[comp_idx["T"]] == pos[comp_idx["F"]] - 1,  # T immediately before F
    pos[comp_idx["R"]] == pos[comp_idx["T"]] - 1   # T immediately after R
))

# Separation constraint for F and R: at least two compositions between them (distance >= 3)
solver.add(Abs(pos[comp_idx["F"]] - pos[comp_idx["R"]]) >= 3)

# O position constraint: first or fifth
solver.add(Or(pos[comp_idx["O"]] == 1, pos[comp_idx["O"]] == 5))

# Eighth-slot constraint: L or H is eighth
solver.add(Or(pos[comp_idx["L"]] == 8, pos[comp_idx["H"]] == 8))

# P-before-S constraint
solver.add(pos[comp_idx["P"]] < pos[comp_idx["S"]])

# O-S separation constraint: at least one composition between them (distance >= 2)
solver.add(Abs(pos[comp_idx["O"]] - pos[comp_idx["S"]]) >= 2)

# Answer choices
answer_choices = [
    ["L", "P", "S", "R", "O", "T", "F", "H"],
    ["O", "T", "P", "F", "S", "H", "R", "L"],
    ["P", "T", "F", "S", "L", "R", "O", "H"],
    ["P", "T", "F", "S", "O", "R", "L", "H"],
    ["T", "F", "P", "R", "O", "L", "S", "H"]
]

# Check each answer choice
satisfiable_indices = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert the fixed ordering from the choice
    for i, comp in enumerate(choice):
        s_chk.add(pos[comp_idx[comp]] == i + 1)
    
    if s_chk.check() == sat:
        satisfiable_indices.append(idx)

print(satisfiable_indices)