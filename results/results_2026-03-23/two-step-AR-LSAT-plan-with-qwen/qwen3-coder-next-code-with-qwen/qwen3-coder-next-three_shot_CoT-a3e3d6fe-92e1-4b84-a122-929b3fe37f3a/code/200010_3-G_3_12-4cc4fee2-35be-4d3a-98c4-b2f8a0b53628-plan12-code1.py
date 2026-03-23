from z3 import *

# Compositions
compositions = ["F", "H", "L", "O", "P", "R", "S", "T"]

# Position variables: pos[comp] = position index (0-7)
pos = {c: Int(f"pos_{c}") for c in compositions}

# Base solver
solver = Solver()

# Distinctness constraint: all positions are distinct (0-7)
solver.add(Distinct(*pos.values()))
for c in compositions:
    solver.add(pos[c] >= 0, pos[c] <= 7)

# Condition a: T immediately before F OR T immediately after R
solver.add(Or(pos["T"] == pos["F"] - 1, pos["T"] == pos["R"] + 1))

# Condition b: At least two between F and R
solver.add(Or(pos["F"] <= pos["R"] - 3, pos["F"] >= pos["R"] + 3))

# Condition c: O first or fifth
solver.add(Or(pos["O"] == 0, pos["O"] == 4))

# Condition d: Eighth is L or H
solver.add(Or(pos["L"] == 7, pos["H"] == 7))

# Condition e: P before S
solver.add(pos["P"] < pos["S"])

# Condition f: At least one between O and S
solver.add(Or(pos["O"] <= pos["S"] - 2, pos["O"] >= pos["S"] + 2))

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
for idx, seq in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert positions based on the sequence
    for i, comp in enumerate(seq):
        s_chk.add(pos[comp] == i)
    
    if s_chk.check() == sat:
        valid_indices.append(idx)

# Print the index of the only valid choice
print(valid_indices[0] if len(valid_indices) == 1 else valid_indices)