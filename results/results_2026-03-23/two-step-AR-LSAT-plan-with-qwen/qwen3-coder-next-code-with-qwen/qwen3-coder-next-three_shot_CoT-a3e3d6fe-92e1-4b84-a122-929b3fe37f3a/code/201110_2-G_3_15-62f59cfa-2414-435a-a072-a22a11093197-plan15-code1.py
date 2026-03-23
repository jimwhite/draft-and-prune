from z3 import *

# Rider indices: 0-Reynaldo, 1-Seamus, 2-Theresa, 3-Yuki
# Bicycle indices: 0-F, 1-G, 2-H, 3-J

# r1[i][j] = True if rider i tests bicycle j on day 1
r1 = [[Bool(f"r1_{i}_{j}") for j in range(4)] for i in range(4)]
# r2[i][j] = True if rider i tests bicycle j on day 2
r2 = [[Bool(f"r2_{i}_{j}") for j in range(4)] for i in range(4)]

solver = Solver()

# Day 1: each rider assigned exactly one bicycle, each bicycle used by exactly one rider
for i in range(4):
    solver.add(AtMost(*[r1[i][j] for j in range(4)], 1))
    solver.add(AtLeast(*[r1[i][j] for j in range(4)], 1))
for j in range(4):
    solver.add(AtMost(*[r1[i][j] for i in range(4)], 1))
    solver.add(AtLeast(*[r1[i][j] for i in range(4)], 1))

# Day 2: each rider assigned exactly one bicycle, each bicycle used by exactly one rider
for i in range(4):
    solver.add(AtMost(*[r2[i][j] for j in range(4)], 1))
    solver.add(AtLeast(*[r2[i][j] for j in range(4)], 1))
for j in range(4):
    solver.add(AtMost(*[r2[i][j] for i in range(4)], 1))
    solver.add(AtLeast(*[r2[i][j] for i in range(4)], 1))

# Fixed constraints
# Reynaldo cannot test F (index 0) on either day
solver.add(Not(r1[0][0]), Not(r2[0][0]))

# Yuki cannot test J (index 3) on either day
solver.add(Not(r1[3][3]), Not(r2[3][3]))

# Theresa must test H (index 2) on at least one day
solver.add(Or(r1[2][2], r2[2][2]))

# The bicycle Yuki tests on day 1 must be tested by Seamus on day 2
for j in range(4):
    solver.add(Implies(r1[3][j], r2[1][j]))

# Answer choices
answer_choices = [
    ("Reynaldo tests J on the first day.", r1[0][3]),  # A
    ("Reynaldo tests J on the second day.", r2[0][3]), # B
    ("Seamus tests H on the first day.", r1[1][2]),    # C
    ("Yuki tests H on the first day.", r1[3][2]),      # D
    ("Yuki tests H on the second day.", r2[3][2])      # E
]

# Check each answer choice
answer_index_list = []
for idx, (_, constraint) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(constraint)
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list[0])