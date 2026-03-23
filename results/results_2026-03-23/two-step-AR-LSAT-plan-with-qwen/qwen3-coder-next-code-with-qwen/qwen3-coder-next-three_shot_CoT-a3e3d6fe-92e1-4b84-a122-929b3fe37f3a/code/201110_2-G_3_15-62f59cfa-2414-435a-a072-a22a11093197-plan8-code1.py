from z3 import *

# Riders: 0-Reynaldo, 1-Seamus, 2-Theresa, 3-Yuki
# Bicycles: 0-F, 1-G, 2-H, 3-J

# First day assignments for each rider
d1 = [Int(f"d1_{i}") for i in range(4)]
# Second day assignments for each rider
d2 = [Int(f"d2_{i}") for i in range(4)]

# Base solver
solver = Solver()

# Domain constraints: each assignment is between 0 and 3
for i in range(4):
    solver.add(d1[i] >= 0, d1[i] <= 3)
    solver.add(d2[i] >= 0, d2[i] <= 3)

# Bijective constraints: each day uses all bicycles exactly once
solver.add(Distinct(d1))
solver.add(Distinct(d2))

# Fixed constraints:
# Reynaldo cannot test F on either day
solver.add(d1[0] != 0)
solver.add(d2[0] != 0)

# Yuki cannot test J on first day
solver.add(d1[3] != 3)

# Theresa must test H on first day
solver.add(d1[2] == 2)

# Yuki's first-day bicycle must be tested by Seamus on second day
solver.add(d2[1] == d1[3])

# Answer choices (EXCEPT means the one that cannot be true)
answer_index_list = []

# Choice 0: Reynaldo tests J on first day (d1[0] == 3)
s_chk = Solver()
s_chk.add(solver.assertions())
s_chk.add(d1[0] == 3)
if s_chk.check() == unsat:
    answer_index_list.append(0)

# Choice 1: Reynaldo tests J on second day (d2[0] == 3)
s_chk = Solver()
s_chk.add(solver.assertions())
s_chk.add(d2[0] == 3)
if s_chk.check() == unsat:
    answer_index_list.append(1)

# Choice 2: Seamus tests H on first day (d1[1] == 2)
s_chk = Solver()
s_chk.add(solver.assertions())
s_chk.add(d1[1] == 2)
if s_chk.check() == unsat:
    answer_index_list.append(2)

# Choice 3: Yuki tests H on first day (d1[3] == 2)
s_chk = Solver()
s_chk.add(solver.assertions())
s_chk.add(d1[3] == 2)
if s_chk.check() == unsat:
    answer_index_list.append(3)

# Choice 4: Yuki tests H on second day (d2[3] == 2)
s_chk = Solver()
s_chk.add(solver.assertions())
s_chk.add(d2[3] == 2)
if s_chk.check() == unsat:
    answer_index_list.append(4)

print(answer_index_list)