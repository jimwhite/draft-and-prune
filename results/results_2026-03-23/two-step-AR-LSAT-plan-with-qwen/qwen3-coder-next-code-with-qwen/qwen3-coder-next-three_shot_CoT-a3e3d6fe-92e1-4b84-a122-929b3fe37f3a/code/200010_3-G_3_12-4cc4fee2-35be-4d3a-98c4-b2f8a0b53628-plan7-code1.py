from z3 import *

# Compositions indices: F, H, L, O, P, R, S, T
compositions = ["F", "H", "L", "O", "P", "R", "S", "T"]
pos = {c: Int(f"pos_{c}") for c in compositions}

# Base solver
solver = Solver()

# Domain constraints: positions 1-8, all distinct
for c in compositions:
    solver.add(pos[c] >= 1, pos[c] <= 8)
solver.add(Distinct(*[pos[c] for c in compositions]))

# T-F-R adjacency condition: T immediately before F OR T immediately after R
solver.add(Or(pos["T"] + 1 == pos["F"], pos["R"] + 1 == pos["T"]))

# Spacing condition for F and R: at least two compositions between them
solver.add(Or(pos["F"] - pos["R"] >= 3, pos["R"] - pos["F"] >= 3))

# O position constraint: O is either first or fifth
solver.add(Or(pos["O"] == 1, pos["O"] == 5))

# Eighth position constraint: L or H is eighth
solver.add(Or(pos["L"] == 8, pos["H"] == 8))

# P-before-S condition
solver.add(pos["P"] < pos["S"])

# O-S separation condition: at least one composition between them
solver.add(Or(pos["O"] - pos["S"] >= 2, pos["S"] - pos["O"] >= 2))

# Answer choices
answer_choices = [
    ["L", "P", "S", "R", "O", "T", "F", "H"],
    ["O", "T", "P", "F", "S", "H", "R", "L"],
    ["P", "T", "F", "S", "L", "R", "O", "H"],
    ["P", "T", "F", "S", "O", "R", "L", "H"],
    ["T", "F", "P", "R", "O", "L", "S", "H"]
]

# Check each answer choice
valid_indices = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add constraints for this specific sequence
    for i, comp in enumerate(choice):
        s_chk.add(pos[comp] == i + 1)
    
    if s_chk.check() == sat:
        valid_indices.append(idx)

print(valid_indices)