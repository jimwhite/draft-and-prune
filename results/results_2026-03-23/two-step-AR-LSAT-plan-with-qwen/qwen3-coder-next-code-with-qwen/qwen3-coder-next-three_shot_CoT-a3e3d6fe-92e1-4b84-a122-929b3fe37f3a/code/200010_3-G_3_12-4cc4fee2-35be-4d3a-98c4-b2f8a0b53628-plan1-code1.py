from z3 import *

# Compositions: F, H, L, O, P, R, S, T
compositions = ["F", "H", "L", "O", "P", "R", "S", "T"]
pos = {comp: Int(f"pos_{comp}") for comp in compositions}

# Base solver
solver = Solver()

# All-different constraint: each composition performed exactly once
solver.add(Distinct(*pos.values()))

# Domain constraints: positions 0 to 7 (representing 1st to 8th)
for comp in compositions:
    solver.add(pos[comp] >= 0, pos[comp] <= 7)

# Condition 1: T is either immediately before F or immediately after R
solver.add(Or(pos["T"] == pos["F"] - 1, pos["T"] == pos["R"] + 1))

# Condition 2: At least two compositions between F and R
solver.add(Abs(pos["F"] - pos["R"]) >= 3)

# Condition 3: O is performed first or fifth (positions 0 or 4)
solver.add(Or(pos["O"] == 0, pos["O"] == 4))

# Condition 4: Eighth composition is L or H (position 7)
solver.add(Or(pos["L"] == 7, pos["H"] == 7))

# Condition 5: P before S
solver.add(pos["P"] < pos["S"])

# Condition 6: At least one composition between O and S
solver.add(Abs(pos["O"] - pos["S"]) >= 2)

# Answer choices
answer_choices = [
    "L, P, S, R, O, T, F, H",
    "O, T, P, F, S, H, R, L",
    "P, T, F, S, L, R, O, H",
    "P, T, F, S, O, R, L, H",
    "T, F, P, R, O, L, S, H"
]

# Check each answer choice
valid_indices = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Parse the choice and add position constraints
    seq = [comp.strip() for comp in choice.split(",")]
    for i, comp in enumerate(seq):
        s_chk.add(pos[comp] == i)
    
    if s_chk.check() == sat:
        valid_indices.append(idx)

# Output the index of the valid sequence
print(valid_indices[0] if valid_indices else -1)