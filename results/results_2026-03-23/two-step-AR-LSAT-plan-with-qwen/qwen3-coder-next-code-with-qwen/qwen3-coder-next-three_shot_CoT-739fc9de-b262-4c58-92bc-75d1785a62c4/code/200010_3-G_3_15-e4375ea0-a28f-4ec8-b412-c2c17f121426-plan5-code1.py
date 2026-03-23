from z3 import *

# Compositions: F, H, L, O, P, R, S, T
comps = ["F", "H", "L", "O", "P", "R", "S", "T"]
pos = {c: Int(f"pos_{c}") for c in comps}

solver = Solver()

# Domain constraints: positions 0-7 (1-based: 1-8)
for c in comps:
    solver.add(pos[c] >= 0, pos[c] <= 7)

# All-different constraint
solver.add(Distinct(*[pos[c] for c in comps]))

# O is performed first or fifth (0-indexed: 0 or 4)
solver.add(Or(pos["O"] == 0, pos["O"] == 4))

# Eighth composition is L or H (position index 7)
solver.add(Or(pos["L"] == 7, pos["H"] == 7))

# P before S
solver.add(pos["P"] < pos["S"])

# At least two compositions between F and R: |pos_F - pos_R| >= 3
solver.add(Or(pos["F"] <= pos["R"] - 3, pos["F"] >= pos["R"] + 3))

# T is immediately before F or immediately after R
solver.add(Or(pos["T"] + 1 == pos["F"], pos["R"] + 1 == pos["T"]))

# At least one composition between O and S: |pos_O - pos_S| >= 2
solver.add(Or(pos["O"] <= pos["S"] - 2, pos["O"] >= pos["S"] + 2))

# Add assumption: O is performed immediately after T → pos_O == pos_T + 1
solver.add(pos["O"] == pos["T"] + 1)

# Since O ∈ {0,4} and pos_O == pos_T + 1, O cannot be 0 (would require T=-1)
# So O must be 4 and T must be 3
solver.add(pos["O"] == 4)
solver.add(pos["T"] == 3)

# With T=3, the adjacency constraint (T+1=F or R+1=T) becomes:
# Either 4 == pos_F (conflict with O=4), or pos_R + 1 == 3 → pos_R = 2
# So we must have pos_R = 2
solver.add(pos["R"] == 2)

# Now check feasible positions for F (excluding used: R=2, T=3, O=4)
feasible_F_positions = []
for i in range(8):
    if i in [2, 3, 4]:
        continue
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(pos["F"] == i)
    if s_chk.check() == sat:
        feasible_F_positions.append(i)

# Convert to 1-based positions
feasible_1_based = [p + 1 for p in feasible_F_positions]

# Map to answer choices
choices = [
    "first or second",      # positions 1,2 → indices [0,1]
    "second or third",      # positions 2,3 → indices [1,2]
    "fourth or sixth",      # positions 4,6 → indices [3,5]
    "fourth or seventh",    # positions 4,7 → indices [3,6]
    "sixth or seventh"      # positions 6,7 → indices [5,6]
]

# Find matching choice index
answer_index = -1
for idx, choice in enumerate(choices):
    if idx == 4:  # "sixth or seventh"
        if set(feasible_1_based) <= {6, 7} and len(set(feasible_1_based)) == 2:
            answer_index = idx
            break

print(answer_index)