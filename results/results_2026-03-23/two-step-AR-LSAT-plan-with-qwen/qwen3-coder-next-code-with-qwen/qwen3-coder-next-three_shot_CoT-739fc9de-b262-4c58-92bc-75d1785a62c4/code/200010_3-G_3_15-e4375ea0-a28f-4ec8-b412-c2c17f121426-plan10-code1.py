from z3 import *

# Compositions indices: F=0, H=1, L=2, O=3, P=4, R=5, S=6, T=7
compositions = ["F", "H", "L", "O", "P", "R", "S", "T"]
pos = {c: Int(f"pos_{c}") for c in compositions}

solver = Solver()

# Domain constraints
for c in compositions:
    solver.add(pos[c] >= 1, pos[c] <= 8)
solver.add(Distinct(*[pos[c] for c in compositions]))

# T is performed either immediately before F or immediately after R
solver.add(Or(pos["T"] == pos["F"] - 1, pos["T"] == pos["R"] + 1))

# At least two compositions between F and R
solver.add(Or(pos["F"] >= pos["R"] + 3, pos["R"] >= pos["F"] + 3))

# O is performed either first or fifth
solver.add(Or(pos["O"] == 1, pos["O"] == 5))

# Eighth composition is L or H
solver.add(Or(pos["L"] == 8, pos["H"] == 8))

# P before S
solver.add(pos["P"] < pos["S"])

# At least one composition between O and S
solver.add(Or(pos["O"] >= pos["S"] + 2, pos["S"] >= pos["O"] + 2))

# Add assumption: O is performed immediately after T
solver.add(pos["O"] == pos["T"] + 1)

# Check if the assumption leads to a unique position for F
s_chk = Solver()
s_chk.add(solver.assertions())

# Force O=5 and T=4 (deduced logically, but we'll let Z3 derive it)
# Actually, we can add the deduction directly: O=5 and T=4
s_chk.add(pos["O"] == 5, pos["T"] == 4)

# From T=R+1 (since T=F-1 would imply F=5, conflict with O=5)
s_chk.add(pos["T"] == pos["R"] + 1)

# Check if F must be at position 6
s_chk_F_not_6 = Solver()
s_chk_F_not_6.add(s_chk.assertions())
s_chk_F_not_6.add(pos["F"] != 6)

if s_chk_F_not_6.check() == unsat:
    # F must be 6, so check which option contains 6
    result = "fourth or sixth"
else:
    # F could be elsewhere, need to find all possible positions for F
    s_chk_F = Solver()
    s_chk_F.add(s_chk.assertions())
    
    possible_positions = []
    for p in range(1, 9):
        s_chk_test = Solver()
        s_chk_test.add(s_chk_F.assertions())
        s_chk_test.add(pos["F"] == p)
        if s_chk_test.check() == sat:
            possible_positions.append(p)
    
    # Check which option matches the possible positions
    options = [
        ("first or second", [1, 2]),
        ("second or third", [2, 3]),
        ("fourth or sixth", [4, 6]),
        ("fourth or seventh", [4, 7]),
        ("sixth or seventh", [6, 7])
    ]
    
    for opt_name, opt_positions in options:
        if set(possible_positions).issubset(set(opt_positions)) and len(possible_positions) > 0:
            result = opt_name
            break

print(result)