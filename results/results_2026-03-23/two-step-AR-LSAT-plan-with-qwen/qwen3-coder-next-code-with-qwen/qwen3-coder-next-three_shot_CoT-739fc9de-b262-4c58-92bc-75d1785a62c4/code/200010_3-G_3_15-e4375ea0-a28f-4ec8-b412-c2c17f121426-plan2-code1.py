from z3 import *

# Compositions indices
compositions = ["F", "H", "L", "O", "P", "R", "S", "T"]
pos = {c: Int(f"pos_{c}") for c in compositions}

# Base solver
solver = Solver()

# Domain constraints: positions 1-8, all distinct
for c in compositions:
    solver.add(pos[c] >= 1, pos[c] <= 8)
solver.add(Distinct(*[pos[c] for c in compositions]))

# Core constraints
## T is performed either immediately before F or immediately after R
solver.add(Or(pos["T"] + 1 == pos["F"], pos["R"] + 1 == pos["T"]))

## At least two compositions between F and R
solver.add(Or(pos["F"] < pos["R"] - 2, pos["R"] < pos["F"] - 2))

## O is performed either first or fifth
solver.add(Or(pos["O"] == 1, pos["O"] == 5))

## Eighth composition is either L or H
solver.add(Or(pos["L"] == 8, pos["H"] == 8))

## P is performed before S
solver.add(pos["P"] < pos["S"])

## At least one composition between O and S
solver.add(Or(pos["O"] < pos["S"] - 1, pos["S"] < pos["O"] - 1))

# Add the conditional assumption: O is performed immediately after T
solver.add(pos["O"] == pos["T"] + 1)

# Check feasible positions for F
feasible_positions = []
for k in range(1, 9):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(pos["F"] == k)
    
    if s_chk.check() == sat:
        feasible_positions.append(k)

# Define answer choices as sets of positions
answer_choices = [
    {1, 2},   # first or second
    {2, 3},   # second or third
    {4, 6},   # fourth or sixth
    {4, 7},   # fourth or seventh
    {6, 7}    # sixth or seventh
]

# Find which choice matches exactly the feasible positions for F
answer_index_list = []
for idx, choice_set in enumerate(answer_choices):
    if set(feasible_positions) == choice_set:
        answer_index_list.append(idx)

print(answer_index_list)