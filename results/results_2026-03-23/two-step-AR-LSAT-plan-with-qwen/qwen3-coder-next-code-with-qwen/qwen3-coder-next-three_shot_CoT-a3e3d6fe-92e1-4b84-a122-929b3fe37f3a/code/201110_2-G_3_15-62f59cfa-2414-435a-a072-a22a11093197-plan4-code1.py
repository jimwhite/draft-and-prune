from z3 import *

# Rider indices: 0-Reynaldo, 1-Seamus, 2-Theresa, 3-Yuki
# Bicycle indices: 0-F, 1-G, 2-H, 3-J

# Day 1 and Day 2 assignment variables
d1 = [[Bool(f"d1_{r}_{b}") for b in range(4)] for r in range(4)]
d2 = [[Bool(f"d2_{r}_{b}") for b in range(4)] for r in range(4)]

solver = Solver()

# Per-day assignment constraints: each rider tests exactly one bicycle per day
for r in range(4):
    solver.add(Sum([If(d1[r][b], 1, 0) for b in range(4)]) == 1)
    solver.add(Sum([If(d2[r][b], 1, 0) for b in range(4)]) == 1)

# Per-day assignment constraints: each bicycle is tested by exactly one rider per day
for b in range(4):
    solver.add(Sum([If(d1[r][b], 1, 0) for r in range(4)]) == 1)
    solver.add(Sum([If(d2[r][b], 1, 0) for r in range(4)]) == 1)

# Explicit condition constraints
# Reynaldo cannot test F (day 1 and day 2)
solver.add(Not(d1[0][0]))
solver.add(Not(d2[0][0]))

# Yuki cannot test J (day 1 and day 2)
solver.add(Not(d1[3][3]))
solver.add(Not(d2[3][3]))

# Theresa must test H on at least one day
solver.add(Or(d1[2][2], d2[2][2]))

# The bicycle Yuki tests on day 1 must be tested by Seamus on day 2
for b in range(4):
    solver.add(Implies(d1[3][b], d2[1][b]))

# Answer choices
# A. Reynaldo tests J on day 1: d1[0][3]
# B. Reynaldo tests J on day 2: d2[0][3]
# C. Seamus tests H on day 1: d1[1][2]
# D. Yuki tests H on day 1: d1[3][2]
# E. Yuki tests H on day 2: d2[3][2]

impossible_indices = []

# Check each choice
for idx, prop in enumerate([
    d1[0][3],  # A: Reynaldo tests J on day 1
    d2[0][3],  # B: Reynaldo tests J on day 2
    d1[1][2],  # C: Seamus tests H on day 1
    d1[3][2],  # D: Yuki tests H on day 1
    d2[3][2]   # E: Yuki tests H on day 2
]):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(prop)
    
    if s_chk.check() == unsat:
        impossible_indices.append(idx)

print(impossible_indices)