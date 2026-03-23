from z3 import *

# Compositions indices: F=0, H=1, L=2, O=3, P=4, R=5, S=6, T=7
compositions = ["F", "H", "L", "O", "P", "R", "S", "T"]

# Position variables
pos = {comp: Int(f"pos_{comp}") for comp in compositions}

# Base solver
solver = Solver()

# Distinctness constraint: all positions are distinct (0-7)
solver.add(Distinct(*pos.values()))
for comp in compositions:
    solver.add(pos[comp] >= 0, pos[comp] <= 7)

# T-F-R adjacency constraint: either (T immediately before F) OR (R immediately before T)
solver.add(Or(
    pos["T"] == pos["F"] - 1,
    pos["R"] == pos["T"] - 1
))

# Separation constraint for F and R: at least two compositions between them
solver.add(Or(
    pos["F"] <= pos["R"] - 3,
    pos["R"] <= pos["F"] - 3
))

# O position constraint: first (0) or fifth (4)
solver.add(Or(pos["O"] == 0, pos["O"] == 4))

# Eighth position constraint: L or H is eighth (position 7)
solver.add(Or(pos["L"] == 7, pos["H"] == 7))

# P-before-S constraint
solver.add(pos["P"] < pos["S"])

# O-S separation with at least one in between: |pos_O - pos_S| >= 2
solver.add(Or(
    pos["O"] <= pos["S"] - 2,
    pos["S"] <= pos["O"] - 2
))

# Answer choices (each is a list of compositions in order from first to eighth)
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
    
    # Assert the exact ordering from the choice
    for i, comp in enumerate(choice):
        s_chk.add(pos[comp] == i)
    
    if s_chk.check() == sat:
        valid_indices.append(idx)

print(valid_indices)