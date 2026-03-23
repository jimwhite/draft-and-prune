from z3 import *

# Rider indices: 0-Reynaldo, 1-Seamus, 2-Theresa, 3-Yuki
# Bicycle indices: 0-F, 1-G, 2-H, 3-J

# d1[r][b] = True if rider r tests bicycle b on day 1
d1 = [[Bool(f"d1_{r}_{b}") for b in range(4)] for r in range(4)]
# d2[r][b] = True if rider r tests bicycle b on day 2
d2 = [[Bool(f"d2_{r}_{b}") for b in range(4)] for r in range(4)]

solver = Solver()

# Day 1 assignment constraints
for r in range(4):
    solver.add(Sum([If(d1[r][b], 1, 0) for b in range(4)]) == 1)
for b in range(4):
    solver.add(Sum([If(d1[r][b], 1, 0) for r in range(4)]) == 1)

# Day 2 assignment constraints
for r in range(4):
    solver.add(Sum([If(d2[r][b], 1, 0) for b in range(4)]) == 1)
for b in range(4):
    solver.add(Sum([If(d2[r][b], 1, 0) for r in range(4)]) == 1)

# Repetition constraint: each rider tests different bicycles on day 2 than day 1
for r in range(4):
    for b in range(4):
        solver.add(Implies(d1[r][b], Not(d2[r][b])))

# Specific condition constraints
# Reynaldo cannot test F on either day
solver.add(Not(d1[0][0]), Not(d2[0][0]))

# Yuki cannot test J on either day
solver.add(Not(d1[3][3]), Not(d2[3][3]))

# Theresa must test H on at least one day
solver.add(Or(d1[2][2], d2[2][2]))

# The bicycle Yuki tests on day 1 must be tested by Seamus on day 2
for b in range(4):
    solver.add(d1[3][b] == d2[1][b])

# Answer choices: each choice is (rider1, rider2, bicycle)
answer_choices = [
    (0, 1, 3),  # Both Reynaldo and Seamus test J
    (0, 2, 3),  # Both Reynaldo and Theresa test J
    (0, 3, 1),  # Both Reynaldo and Yuki test G
    (1, 2, 1),  # Both Seamus and Theresa test G
    (2, 3, 0)   # Both Theresa and Yuki test F
]

# Check each answer choice
answer_index_list = []
for idx, (r1, r2, b) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Both riders must test the specified bicycle (on at least one day each)
    s_chk.add(Or(d1[r1][b], d2[r1][b]))
    s_chk.add(Or(d1[r2][b], d2[r2][b]))
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)