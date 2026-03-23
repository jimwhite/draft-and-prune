from z3 import *

# Compositions: F, H, L, O, P, R, S, T
compositions = ["F", "H", "L", "O", "P", "R", "S", "T"]
pos = {c: Int(f"pos_{c}") for c in compositions}

solver = Solver()

# Domain constraints
for c in compositions:
    solver.add(pos[c] >= 1, pos[c] <= 8)
solver.add(Distinct(*[pos[c] for c in compositions]))

# T immediately before F OR T immediately after R
solver.add(Or(pos["T"] + 1 == pos["F"], pos["R"] + 1 == pos["T"]))

# At least two compositions between F and R
solver.add(Or(pos["F"] + 2 <= pos["R"], pos["R"] + 2 <= pos["F"]))

# O is first or fifth
solver.add(Or(pos["O"] == 1, pos["O"] == 5))

# Eighth composition is L or H
solver.add(Or(pos["L"] == 8, pos["H"] == 8))

# P before S
solver.add(pos["P"] < pos["S"])

# At least one composition between O and S
solver.add(Or(pos["O"] + 1 < pos["S"], pos["S"] + 1 < pos["O"]))

# Premise: O is performed immediately after T
solver.add(pos["O"] == pos["T"] + 1)

# Find all possible positions for F
feasible_positions = []
for f in range(1, 9):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(pos["F"] == f)
    if s_chk.check() == sat:
        feasible_positions.append(f)

# Map positions to answer choices
# Choices: 
# 0: 'first or second' -> [1,2]
# 1: 'second or third' -> [2,3]
# 2: 'fourth or sixth' -> [4,6]
# 3: 'fourth or seventh' -> [4,7]
# 4: 'sixth or seventh' -> [6,7]

answer_options = [
    {1, 2},
    {2, 3},
    {4, 6},
    {4, 7},
    {6, 7}
]

feasible_set = set(feasible_positions)

# Find which option matches exactly
result_indices = []
for idx, opt in enumerate(answer_options):
    if feasible_set == opt:
        result_indices.append(idx)

# Output the corresponding answer string
if result_indices:
    # Map index to actual choice text
    choice_texts = [
        'first or second',
        'second or third',
        'fourth or sixth',
        'fourth or seventh',
        'sixth or seventh'
    ]
    print(choice_texts[result_indices[0]])
else:
    # If no exact match (shouldn't happen), print feasible positions for debugging
    print(feasible_positions)