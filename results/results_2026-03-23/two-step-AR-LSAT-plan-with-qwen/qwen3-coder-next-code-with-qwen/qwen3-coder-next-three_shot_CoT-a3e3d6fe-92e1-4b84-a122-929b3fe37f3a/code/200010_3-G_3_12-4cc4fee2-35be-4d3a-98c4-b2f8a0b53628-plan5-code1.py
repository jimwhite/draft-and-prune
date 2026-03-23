from z3 import *

# Compositions
compositions = ["F", "H", "L", "O", "P", "R", "S", "T"]

# Position variables (1-based)
pos = {c: Int(f"pos_{c}") for c in compositions}

# Base solver
solver = Solver()

# Domain and permutation constraints
for c in compositions:
    solver.add(pos[c] >= 1, pos[c] <= 8)
solver.add(Distinct(*[pos[c] for c in compositions]))

# T-F-R adjacency constraint: (T immediately before F) OR (R immediately before T)
solver.add(Or(pos["T"] + 1 == pos["F"], pos["R"] + 1 == pos["T"]))

# At least two compositions between F and R: |pos_F - pos_R| >= 3
solver.add(Or(pos["F"] + 3 <= pos["R"], pos["R"] + 3 <= pos["F"]))

# O is first or fifth
solver.add(Or(pos["O"] == 1, pos["O"] == 5))

# Eighth position is L or H
solver.add(Or(pos["L"] == 8, pos["H"] == 8))

# P before S
solver.add(pos["P"] < pos["S"])

# At least one composition between O and S: |pos_O - pos_S| >= 2
solver.add(Or(pos["O"] + 2 <= pos["S"], pos["S"] + 2 <= pos["O"]))

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
    
    # Add constraints matching the proposed sequence
    for i, c in enumerate(choice):
        s_chk.add(pos[c] == i + 1)
    
    if s_chk.check() == sat:
        valid_indices.append(idx)

# Output the first valid index (as per question format)
print(valid_indices[0] if valid_indices else -1)