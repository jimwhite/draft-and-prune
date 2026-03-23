from z3 import *

# Rider indices: 0-Reynaldo, 1-Seamus, 2-Theresa, 3-Yuki
# Bicycle indices: 0-F, 1-G, 2-H, 3-J

# First day assignment: first[i][j] = True if rider i tests bicycle j on day 1
first = [[Bool(f"first_{i}_{j}") for j in range(4)] for i in range(4)]

# Second day assignment: second[i][j] = True if rider i tests bicycle j on day 2
second = [[Bool(f"second_{i}_{j}") for j in range(4)] for i in range(4)]

solver = Solver()

# Day 1 constraints: each rider tests exactly one bicycle, each bicycle tested by exactly one rider
for i in range(4):
    solver.add(PbAtLeast(*[(first[i][j], 1) for j in range(4)], 1))
    solver.add(PbAtMost(*[(first[i][j], 1) for j in range(4)], 1))
for j in range(4):
    solver.add(PbAtLeast(*[(first[i][j], 1) for i in range(4)], 1))
    solver.add(PbAtMost(*[(first[i][j], 1) for i in range(4)], 1))

# Day 2 constraints: each rider tests exactly one bicycle, each bicycle tested by exactly one rider
for i in range(4):
    solver.add(PbAtLeast(*[(second[i][j], 1) for j in range(4)], 1))
    solver.add(PbAtMost(*[(second[i][j], 1) for j in range(4)], 1))
for j in range(4):
    solver.add(PbAtLeast(*[(second[i][j], 1) for i in range(4)], 1))
    solver.add(PbAtMost(*[(second[i][j], 1) for i in range(4)], 1))

# Given condition constraints
# Reynaldo (0) cannot test F (0) on either day
solver.add(Not(first[0][0]))
solver.add(Not(second[0][0]))

# Yuki (3) cannot test J (3) on day 1
solver.add(Not(first[3][3]))

# Theresa (2) must test H (2) on at least one day
solver.add(Or(first[2][2], second[2][2]))

# The bicycle Yuki tests on day 1 must be tested by Seamus (1) on day 2
for j in range(4):
    solver.add(Implies(first[3][j], second[1][j]))

# Choices: A-Reynaldo tests J on day 1, B-Reynaldo tests J on day 2, C-Seamus tests H on day 1,
#          D-Yuki tests H on day 1, E-Yuki tests H on day 2
# Indices: 0, 1, 2, 3, 4 respectively

forbidden_index_list = []

# Choice A: Reynaldo tests J on day 1 (first[0][3])
s_chk = Solver()
s_chk.add(solver.assertions())
s_chk.add(first[0][3])
if s_chk.check() == unsat:
    forbidden_index_list.append(0)

# Choice B: Reynaldo tests J on day 2 (second[0][3])
s_chk = Solver()
s_chk.add(solver.assertions())
s_chk.add(second[0][3])
if s_chk.check() == unsat:
    forbidden_index_list.append(1)

# Choice C: Seamus tests H on day 1 (first[1][2])
s_chk = Solver()
s_chk.add(solver.assertions())
s_chk.add(first[1][2])
if s_chk.check() == unsat:
    forbidden_index_list.append(2)

# Choice D: Yuki tests H on day 1 (first[3][2])
s_chk = Solver()
s_chk.add(solver.assertions())
s_chk.add(first[3][2])
if s_chk.check() == unsat:
    forbidden_index_list.append(3)

# Choice E: Yuki tests H on day 2 (second[3][2])
s_chk = Solver()
s_chk.add(solver.assertions())
s_chk.add(second[3][2])
if s_chk.check() == unsat:
    forbidden_index_list.append(4)

print(forbidden_index_list)