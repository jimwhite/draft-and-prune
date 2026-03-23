from z3 import *

# Compositions
compositions = ["F", "H", "L", "O", "P", "R", "S", "T"]

# Position variables: pos[c] = position (1-8) of composition c
pos = {c: Int(f"pos_{c}") for c in compositions}

# Base solver
solver = Solver()

# Domain constraints: positions are 1-8 and all distinct
for c in compositions:
    solver.add(pos[c] >= 1, pos[c] <= 8)
solver.add(Distinct(*[pos[c] for c in compositions]))

# T-F-R adjacency constraint: T immediately before F OR T immediately after R
solver.add(Or(pos["T"] + 1 == pos["F"], pos["R"] + 1 == pos["T"]))

# Separation constraint: at least two compositions between F and R
solver.add(Or(pos["F"] + 2 <= pos["R"], pos["R"] + 2 <= pos["F"]))

# O position constraint: O is first or fifth
solver.add(Or(pos["O"] == 1, pos["O"] == 5))

# Eighth position constraint: L or H is eighth
solver.add(Or(pos["L"] == 8, pos["H"] == 8))

# P-before-S constraint
solver.add(pos["P"] < pos["S"])

# O-S separation with at least one in between
solver.add(Or(pos["O"] + 1 <= pos["S"], pos["S"] + 1 <= pos["O"]))

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
for idx, order in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert the implied positional equalities
    for i, c in enumerate(order):
        s_chk.add(pos[c] == i + 1)
    
    if s_chk.check() == sat:
        valid_indices.append(idx)

# Print the index of the valid answer (0-indexed)
print(valid_indices[0] if valid_indices else -1)