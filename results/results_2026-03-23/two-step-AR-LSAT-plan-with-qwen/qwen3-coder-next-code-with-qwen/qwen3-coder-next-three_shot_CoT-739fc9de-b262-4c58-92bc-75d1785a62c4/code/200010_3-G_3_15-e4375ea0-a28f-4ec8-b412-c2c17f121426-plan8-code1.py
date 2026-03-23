from z3 import *

# Compositions indices: F=0, H=1, L=2, O=3, P=4, R=5, S=6, T=7
compositions = ["F", "H", "L", "O", "P", "R", "S", "T"]
pos = {c: Int(f"pos_{c}") for c in compositions}

# Base solver
solver = Solver()

# Domain constraints: positions 1-8, all distinct
for c in compositions:
    solver.add(pos[c] >= 1, pos[c] <= 8)
solver.add(Distinct(*[pos[c] for c in compositions]))

# O is performed either first or fifth
solver.add(Or(pos["O"] == 1, pos["O"] == 5))

# Eighth composition is either L or H
solver.add(Or(pos["L"] == 8, pos["H"] == 8))

# P is performed before S
solver.add(pos["P"] < pos["S"])

# At least two compositions between F and R
solver.add(Or(pos["F"] + 2 <= pos["R"], pos["R"] + 2 <= pos["F"]))

# T is performed either immediately before F or immediately after R
solver.add(Or(pos["T"] + 1 == pos["F"], pos["R"] + 1 == pos["T"]))

# At least one composition between O and S
solver.add(Or(pos["O"] + 2 <= pos["S"], pos["S"] + 2 <= pos["O"]))

# Hypothetical: O is performed immediately after T
solver.add(pos["O"] == pos["T"] + 1)

# From O being first or fifth and immediately after T:
# If pos_O = 1, then pos_T = 0 (impossible since positions start at 1)
# So only possibility: pos_O = 5, pos_T = 4
solver.add(pos["O"] == 5)
solver.add(pos["T"] == 4)

# Find all possible positions for F under these constraints
F_possible_positions = []
for p in range(1, 9):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(pos["F"] == p)
    
    if s_chk.check() == sat:
        F_possible_positions.append(p)

# Answer choices with their position sets
answer_options = [
    ([1, 2], "first or second"),
    ([2, 3], "second or third"),
    ([4, 6], "fourth or sixth"),
    ([4, 7], "fourth or seventh"),
    ([6, 7], "sixth or seventh")
]

# Find which option contains all possible F positions
answer_index_list = []
for idx, (positions_set, _) in enumerate(answer_options):
    if all(p in positions_set for p in F_possible_positions) and len(F_possible_positions) > 0:
        answer_index_list.append(idx)

print(answer_index_list)