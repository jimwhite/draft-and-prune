from z3 import *

# Riders: 0-Reynaldo, 1-Seamus, 2-Theresa, 3-Yuki
# Bicycles: 0-F, 1-G, 2-H, 3-J

# r1[i][j] = True if rider i tests bicycle j on day 1
r1 = [[Bool(f"r1_{i}_{j}") for j in range(4)] for i in range(4)]
# r2[i][j] = True if rider i tests bicycle j on day 2
r2 = [[Bool(f"r2_{i}_{j}") for j in range(4)] for i in range(4)]

solver = Solver()

# Day 1: each rider tests exactly one bicycle, each bicycle tested by exactly one rider
for i in range(4):
    solver.add(Sum([If(r1[i][j], 1, 0) for j in range(4)]) == 1)
for j in range(4):
    solver.add(Sum([If(r1[i][j], 1, 0) for i in range(4)]) == 1)

# Day 2: each rider tests exactly one bicycle, each bicycle tested by exactly one rider
for i in range(4):
    solver.add(Sum([If(r2[i][j], 1, 0) for j in range(4)]) == 1)
for j in range(4):
    solver.add(Sum([If(r2[i][j], 1, 0) for i in range(4)]) == 1)

# Forbidden assignments
# Reynaldo (0) cannot test F (0)
solver.add(Not(r1[0][0]), Not(r2[0][0]))
# Yuki (3) cannot test J (3)
solver.add(Not(r1[3][3]), Not(r2[3][3]))

# Theresa (2) must test H (2) on at least one day
solver.add(Or(r1[2][2], r2[2][2]))

# Yuki's day 1 bicycle must be tested by Seamus on day 2
for j in range(4):
    solver.add(Implies(r1[3][j], r2[1][j]))

# Answer choices
answer_choices = [
    ("Reynaldo tests J on the first day", r1[0][3]),
    ("Reynaldo tests J on the second day", r2[0][3]),
    ("Seamus tests H on the first day", r1[1][2]),
    ("Yuki tests H on the first day", r1[3][2]),
    ("Yuki tests H on the second day", r2[3][2])
]

answer_index_list = []
for idx, (_, constraint) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(constraint)
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)