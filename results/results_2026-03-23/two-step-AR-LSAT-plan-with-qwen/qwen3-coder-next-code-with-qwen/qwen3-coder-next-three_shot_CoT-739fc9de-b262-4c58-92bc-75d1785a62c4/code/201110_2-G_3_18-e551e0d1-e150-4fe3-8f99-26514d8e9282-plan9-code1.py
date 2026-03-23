from z3 import *

# Rider indices: 0-Reynaldo, 1-Seamus, 2-Theresa, 3-Yuki
# Bicycle indices: 0-F, 1-G, 2-H, 3-J

# First day assignments: r1[i] = bicycle tested by rider i on day 1
r1 = [Int(f"r1_{i}") for i in range(4)]

# Second day assignments: r2[i] = bicycle tested by rider i on day 2
r2 = [Int(f"r2_{i}") for i in range(4)]

# Base solver
solver = Solver()

# Domain constraints: each assignment must be a bicycle (0-3)
for i in range(4):
    solver.add(r1[i] >= 0, r1[i] <= 3)
    solver.add(r2[i] >= 0, r2[i] <= 3)

# Permutation constraints: each day uses all bicycles exactly once
solver.add(Distinct(r1))
solver.add(Distinct(r2))

# Constraint: Reynaldo cannot test F (bicycle 0)
solver.add(r1[0] != 0)

# Constraint: Yuki cannot test J (bicycle 3)
solver.add(r1[3] != 3)

# Constraint: Theresa must test H (bicycle 2) on at least one day
solver.add(Or(r1[2] == 2, r2[2] == 2))

# Constraint: Yuki's first-day bike = Seamus's second-day bike
solver.add(r1[3] == r2[1])

# Answer choices conditions:
# A. Both Reynaldo and Seamus test J: r1[0] == 3 AND r1[1] == 3
# B. Both Reynaldo and Theresa test J: r1[0] == 3 AND r1[2] == 3
# C. Both Reynaldo and Yuki test G: r1[0] == 1 AND r1[3] == 1
# D. Both Seamus and Theresa test G: r1[1] == 1 AND r1[2] == 1
# E. Both Theresa and Yuki test F: r1[2] == 0 AND r1[3] == 0

answer_conditions = [
    And(r1[0] == 3, r1[1] == 3),  # A
    And(r1[0] == 3, r1[2] == 3),  # B
    And(r1[0] == 1, r1[3] == 1),  # C
    And(r1[1] == 1, r1[2] == 1),  # D
    And(r1[2] == 0, r1[3] == 0)   # E
]

answer_index_list = []

for idx, cond in enumerate(answer_conditions):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(cond)
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)