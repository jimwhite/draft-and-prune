from z3 import *

# Rider indices: 0-Reynaldo, 1-Seamus, 2-Theresa, 3-Yuki
# Bicycle indices: 0-F, 1-G, 2-H, 3-J

# Day 1 assignments: r1[i][b] = True if rider i tests bicycle b on day 1
r1 = [[Bool(f"r1_{i}_{b}") for b in range(4)] for i in range(4)]

# Day 2 assignments: r2[i][b] = True if rider i tests bicycle b on day 2
r2 = [[Bool(f"r2_{i}_{b}") for b in range(4)] for i in range(4)]

solver = Solver()

# Day 1 constraints: each rider tests exactly one bicycle, each bicycle tested by exactly one rider
for i in range(4):
    solver.add(AtMost(*[r1[i][b] for b in range(4)], 1))
    solver.add(AtLeast(*[r1[i][b] for b in range(4)], 1))
for b in range(4):
    solver.add(AtMost(*[r1[i][b] for i in range(4)], 1))
    solver.add(AtLeast(*[r1[i][b] for i in range(4)], 1))

# Day 2 constraints: each rider tests exactly one bicycle, each bicycle tested by exactly one rider
for i in range(4):
    solver.add(AtMost(*[r2[i][b] for b in range(4)], 1))
    solver.add(AtLeast(*[r2[i][b] for b in range(4)], 1))
for b in range(4):
    solver.add(AtMost(*[r2[i][b] for i in range(4)], 1))
    solver.add(AtLeast(*[r2[i][b] for i in range(4)], 1))

# No rider tests the same bicycle on both days
for i in range(4):
    for b in range(4):
        solver.add(Implies(r1[i][b], Not(r2[i][b])))

# Conditional constraints
# Reynaldo cannot test F on day 1
solver.add(Not(r1[0][0]))

# Yuki cannot test J on day 1
solver.add(Not(r1[3][3]))

# Theresa must test H on at least one day
solver.add(Or(r1[2][2], r2[2][2]))

# The bicycle Yuki tests on day 1 must be tested by Seamus on day 2
for b in range(4):
    solver.add(Implies(r1[3][b], r2[1][b]))

# Answer choices (each as a conjunction)
answer_choices = [
    # Both Reynaldo and Seamus test J.
    And(r1[0][3], r1[1][3]),
    # Both Reynaldo and Theresa test J.
    And(r1[0][3], r1[2][3]),
    # Both Reynaldo and Yuki test G.
    And(r1[0][1], r1[3][1]),
    # Both Seamus and Theresa test G.
    And(r1[1][1], r1[2][1]),
    # Both Theresa and Yuki test F.
    And(r1[2][0], r1[3][0])
]

# Check each answer choice
answer_index_list = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(choice)
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)