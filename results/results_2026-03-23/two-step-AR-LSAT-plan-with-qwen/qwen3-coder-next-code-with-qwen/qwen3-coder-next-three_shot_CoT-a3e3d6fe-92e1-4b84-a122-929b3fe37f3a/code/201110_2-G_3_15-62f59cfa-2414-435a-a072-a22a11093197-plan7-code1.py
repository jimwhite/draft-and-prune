from z3 import *

# Riders: 0-Reynaldo, 1-Seamus, 2-Theresa, 3-Yuki
# Bicycles: 0-F, 1-G, 2-H, 3-J

# Day 1 assignments: r1[i][j] = True if rider i tests bicycle j on day 1
r1 = [[Bool(f"r1_{i}_{j}") for j in range(4)] for i in range(4)]

# Day 2 assignments: r2[i][j] = True if rider i tests bicycle j on day 2
r2 = [[Bool(f"r2_{i}_{j}") for j in range(4)] for i in range(4)]

solver = Solver()

# Day 1 constraints: each rider tests exactly one bicycle, each bicycle tested by exactly one rider
for i in range(4):
    solver.add(Sum([If(r1[i][j], 1, 0) for j in range(4)]) == 1)
for j in range(4):
    solver.add(Sum([If(r1[i][j], 1, 0) for i in range(4)]) == 1)

# Day 2 constraints: each rider tests exactly one bicycle, each bicycle tested by exactly one rider
for i in range(4):
    solver.add(Sum([If(r2[i][j], 1, 0) for j in range(4)]) == 1)
for j in range(4):
    solver.add(Sum([If(r2[i][j], 1, 0) for i in range(4)]) == 1)

# Exclusion constraints
# Reynaldo cannot test F (index 0) on any day
solver.add(Not(r1[0][0]), Not(r2[0][0]))
# Yuki cannot test J (index 3) on any day
solver.add(Not(r1[3][3]), Not(r2[3][3]))

# Theresa must test H (index 2) on at least one day
solver.add(Or(r1[2][2], r2[2][2]))

# Yuki's day 1 bicycle must be tested by Seamus on day 2
for j in range(4):
    solver.add(Implies(r1[3][j], r2[1][j]))

# Answer choices (indices 0-4)
answer_choices = [
    ("Reynaldo tests J on day 1", r1[0][3]),      # A
    ("Reynaldo tests J on day 2", r2[0][3]),      # B
    ("Seamus tests H on day 1", r1[1][2]),        # C
    ("Yuki tests H on day 1", r1[3][2]),          # D
    ("Yuki tests H on day 2", r2[3][2])           # E
]

answer_index_list = []
for idx, (_, assertion) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(assertion)
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)