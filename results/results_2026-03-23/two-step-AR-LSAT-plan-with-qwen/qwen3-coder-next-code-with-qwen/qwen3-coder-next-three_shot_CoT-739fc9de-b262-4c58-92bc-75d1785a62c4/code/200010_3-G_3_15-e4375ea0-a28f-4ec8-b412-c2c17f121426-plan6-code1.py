from z3 import *

# Compositions: F=0, H=1, L=2, O=3, P=4, R=5, S=6, T=7
pos = [Int(f"pos_{i}") for i in range(8)]

solver = Solver()

# Domain constraints: positions 1-8, all distinct
for i in range(8):
    solver.add(pos[i] >= 1, pos[i] <= 8)
solver.add(Distinct(*pos))

# T is performed either immediately before F or immediately after R
solver.add(Or(pos[7] + 1 == pos[0], pos[5] + 1 == pos[7]))

# At least two compositions between F and R: |pos_F - pos_R| >= 3
solver.add(Or(pos[0] <= pos[5] - 3, pos[0] >= pos[5] + 3))

# O is performed either first or fifth
solver.add(Or(pos[3] == 1, pos[3] == 5))

# Eighth composition is L or H
solver.add(Or(pos[2] == 8, pos[1] == 8))

# P before S
solver.add(pos[4] < pos[6])

# At least one composition between O and S: |pos_O - pos_S| >= 2
solver.add(Or(pos[3] <= pos[6] - 2, pos[3] >= pos[6] + 2))

# Premise: O is performed immediately after T
solver.add(pos[3] == pos[7] + 1)

# Check possible positions for F
possible_positions = []
for p in range(1, 9):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(pos[0] == p)
    
    if s_chk.check() == sat:
        possible_positions.append(p)

print(possible_positions)