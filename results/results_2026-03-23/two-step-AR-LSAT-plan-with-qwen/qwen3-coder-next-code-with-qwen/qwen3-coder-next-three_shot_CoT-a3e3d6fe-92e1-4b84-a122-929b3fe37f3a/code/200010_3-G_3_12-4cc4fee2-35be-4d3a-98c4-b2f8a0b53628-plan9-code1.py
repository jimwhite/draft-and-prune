from z3 import *

# Compositions
comps = ["F", "H", "L", "O", "P", "R", "S", "T"]

# Position variables: pos[comp] = position (1-8)
pos = {c: Int(f"pos_{c}") for c in comps}

# Base solver
solver = Solver()

# Distinctness constraint: all positions are distinct
solver.add(Distinct(*[pos[c] for c in comps]))

# T is performed either immediately before F or immediately after R
solver.add(Or(pos["T"] == pos["F"] - 1, pos["T"] == pos["R"] + 1))

# At least two compositions are performed either after F and before R, or after R and before F
solver.add(Or(pos["F"] + 2 <= pos["R"], pos["R"] + 2 <= pos["F"]))

# O is performed either first or fifth
solver.add(Or(pos["O"] == 1, pos["O"] == 5))

# The eighth composition is either L or H
solver.add(Or(pos["L"] == 8, pos["H"] == 8))

# P is performed before S
solver.add(pos["P"] < pos["S"])

# At least one composition is performed either after O and before S, or after S and before O
solver.add(Or(pos["O"] < pos["S"] - 1, pos["S"] < pos["O"] - 1))

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
    
    # Assert the sequence positions: first -> 1, second -> 2, ..., eighth -> 8
    for i, comp in enumerate(seq):
        s_chk.add(pos[comp] == i + 1)
    
    if s_chk.check() == sat:
        valid_indices.append(idx)

# Output the valid index (only one should be valid)
print(valid_indices[0] if valid_indices else -1)