from z3 import *

# Compositions: F, H, L, O, P, R, S, T
compositions = ["F", "H", "L", "O", "P", "R", "S", "T"]
pos = {c: Int(f"pos_{c}") for c in compositions}

# Base solver
solver = Solver()

# Domain constraints: positions 1-8
for c in compositions:
    solver.add(pos[c] >= 1, pos[c] <= 8)

# All positions distinct
solver.add(Distinct(*[pos[c] for c in compositions]))

# Constraint (a): T is immediately before F OR immediately after R
solver.add(Or(pos["T"] + 1 == pos["F"], pos["R"] + 1 == pos["T"]))

# Constraint (b): At least two compositions between F and R
solver.add(Or(pos["F"] + 3 <= pos["R"], pos["R"] + 3 <= pos["F"]))

# Constraint (c): O is first or fifth
solver.add(Or(pos["O"] == 1, pos["O"] == 5))

# Constraint (d): Eighth composition is L or H
solver.add(Or(pos["L"] == 8, pos["H"] == 8))

# Constraint (e): P before S
solver.add(pos["P"] < pos["S"])

# Constraint (f): At least one composition between O and S
solver.add(Or(pos["O"] + 2 <= pos["S"], pos["S"] + 2 <= pos["O"]))

# Add the assumption: O is performed immediately after T
solver.add(pos["T"] + 1 == pos["O"])

# From the assumption and constraint (a), we deduce:
# Since O = T+1, if T were immediately before F (T+1=F), then F=O, impossible.
# So must have R immediately before T: R+1=T
# Therefore: R, T, O are consecutive with positions p, p+1, p+2
# And since O ∈ {1,5} and O = p+2 ≥ 3, only possibility is O=5 → R=3, T=4, O=5
# Explicitly enforce these positions to help Z3
solver.add(pos["R"] == 3, pos["T"] == 4, pos["O"] == 5)

# Now find feasible positions for F
feasible_F_positions = []

for k in range(1, 9):
    # Skip positions already taken by R=3, T=4, O=5
    if k in [3, 4, 5]:
        continue
    
    s_chk = Solver()
    # Add all base constraints plus the assumption and fixed positions
    for a in solver.assertions():
        s_chk.add(a)
    
    # Add constraint that F is at position k
    s_chk.add(pos["F"] == k)
    
    if s_chk.check() == sat:
        feasible_F_positions.append(k)

# Answer choices as sets of positions
answer_choices = [
    {1, 2},      # first or second
    {2, 3},      # second or third (but 3 is taken by R)
    {4, 6},      # fourth or sixth (but 4 is taken by T)
    {4, 7},      # fourth or seventh (but 4 is taken by T)
    {6, 7}       # sixth or seventh
]

# Find which choice contains all feasible F positions
answer_index_list = []
for idx, choice in enumerate(answer_choices):
    if set(feasible_F_positions).issubset(choice):
        answer_index_list.append(idx)

print(answer_index_list)