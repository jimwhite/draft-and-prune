from z3 import *

# Rider indices: 0-Reynaldo, 1-Seamus, 2-Theresa, 3-Yuki
# Bicycle indices: 0-F, 1-G, 2-H, 3-J

# Day 1 assignment: r1[i][j] = True if rider i tests bicycle j on day 1
r1 = [[Bool(f"r1_{i}_{j}") for j in range(4)] for i in range(4)]

# Day 2 assignment: r2[i][j] = True if rider i tests bicycle j on day 2
r2 = [[Bool(f"r2_{i}_{j}") for j in range(4)] for i in range(4)]

solver = Solver()

# Day 1 constraints: each rider tests exactly one bicycle, each bicycle tested by exactly one rider
for i in range(4):
    solver.add(PbAtLeast([(r1[i][j], 1) for j in range(4)], 1))
    solver.add(PbAtMost([(r1[i][j], 1) for j in range(4)], 1))
for j in range(4):
    solver.add(PbAtLeast([(r1[i][j], 1) for i in range(4)], 1))
    solver.add(PbAtMost([(r1[i][j], 1) for i in range(4)], 1))

# Day 2 constraints: each rider tests exactly one bicycle, each bicycle tested by exactly one rider
for i in range(4):
    solver.add(PbAtLeast([(r2[i][j], 1) for j in range(4)], 1))
    solver.add(PbAtMost([(r2[i][j], 1) for j in range(4)], 1))
for j in range(4):
    solver.add(PbAtLeast([(r2[i][j], 1) for i in range(4)], 1))
    solver.add(PbAtMost([(r2[i][j], 1) for i in range(4)], 1))

# Repetition restriction: each rider tests a different bicycle on day 2 than on day 1
for i in range(4):
    for j in range(4):
        solver.add(Implies(r1[i][j], Not(r2[i][j])))

# Exclusion constraints
# Reynaldo cannot test F on day 1
solver.add(Not(r1[0][0]))
# Yuki cannot test J on day 1
solver.add(Not(r1[3][3]))

# Theresa must test H on some day (day 1 or day 2)
solver.add(Or(r1[2][2], r2[2][2]))

# Yuki–Seamus dependency: the bicycle Yuki tests on day 1 must be tested by Seamus on day 2
for j in range(4):
    solver.add(Implies(r1[3][j], r2[1][j]))

# Answer choices (EXCEPT question - find which one cannot be true)
answer_choices = [
    ("Reynaldo tests J on the first day.", 0, 3, 1),  # r1[Reynaldo][J] = True
    ("Reynaldo tests J on the second day.", 0, 3, 2), # r2[Reynaldo][J] = True
    ("Seamus tests H on the first day.", 1, 2, 1),     # r1[Seamus][H] = True
    ("Yuki tests H on the first day.", 3, 2, 1),       # r1[Yuki][H] = True
    ("Yuki tests H on the second day.", 3, 2, 2)       # r2[Yuki][H] = True
]

except_index_list = []
for idx, (desc, rider, bike, day) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    if day == 1:
        s_chk.add(r1[rider][bike])
    else:  # day == 2
        s_chk.add(r2[rider][bike])
    
    if s_chk.check() == unsat:
        except_index_list.append(idx)

print(except_index_list)