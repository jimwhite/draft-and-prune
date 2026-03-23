from z3 import *

# Compositions: F, H, L, O, P, R, S, T
comps = ["F", "H", "L", "O", "P", "R", "S", "T"]
pos = {c: Int(f"pos_{c}") for c in comps}

solver = Solver()

# Domain constraints: positions 0-7
for c in comps:
    solver.add(pos[c] >= 0, pos[c] <= 7)

# All positions distinct
solver.add(Distinct(*[pos[c] for c in comps]))

# Base conditions:
# T immediately before F OR T immediately after R
solver.add(Or(pos["T"] + 1 == pos["F"], pos["T"] == pos["R"] + 1))

# At least two compositions between F and R
solver.add(Or(pos["F"] - pos["R"] >= 3, pos["R"] - pos["F"] >= 3))

# O is first (0) or fifth (4)
solver.add(Or(pos["O"] == 0, pos["O"] == 4))

# Eighth position (index 7) is L or H
solver.add(Or(pos["L"] == 7, pos["H"] == 7))

# P before S
solver.add(pos["P"] < pos["S"])

# At least one composition between O and S
solver.add(Or(pos["O"] - pos["S"] >= 2, pos["S"] - pos["O"] >= 2))

# Additional assumption: O is performed immediately after T
solver.add(pos["O"] == pos["T"] + 1)

# Since O must be first (0) or fifth (4), and O = T+1, O cannot be 0 (would require T=-1)
# So O must be 4 and T must be 3
solver.add(pos["O"] == 4)
solver.add(pos["T"] == 3)

# With T=3, the disjunction for T/F/R adjacency:
# If T+1 == F → F=4, but O=4 already → conflict
# So only possibility: T == R+1 → 3 = R+1 → R=2
solver.add(pos["R"] == 2)

# Now check possible positions for F (must satisfy |F - R| >= 3 → |F-2|>=3)
# So F <= -1 (impossible) or F >= 5 → F ∈ {5,6,7}
# But we'll let Z3 determine feasibility

# Check which positions F can take
possible_F_positions = []
for f_pos in range(8):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(pos["F"] == f_pos)
    
    if s_chk.check() == sat:
        possible_F_positions.append(f_pos)

# Convert positions to performance order (1-indexed)
first_or_second = [0, 1]
second_or_third = [1, 2]
fourth_or_sixth = [3, 5]
fourth_or_seventh = [3, 6]
sixth_or_seventh = [5, 6]

# Determine which choice matches the possible F positions
result_choices = []
if set(possible_F_positions) == set(first_or_second):
    result_choices.append("first or second")
elif set(possible_F_positions) == set(second_or_third):
    result_choices.append("second or third")
elif set(possible_F_positions) == set(fourth_or_sixth):
    result_choices.append("fourth or sixth")
elif set(possible_F_positions) == set(fourth_or_seventh):
    result_choices.append("fourth or seventh")
elif set(possible_F_positions) == set(sixth_or_seventh):
    result_choices.append("sixth or seventh")

# Since the question asks "F must be performed either", and we found possible_F_positions,
# we output the matching choice
print(result_choices[0] if result_choices else "")