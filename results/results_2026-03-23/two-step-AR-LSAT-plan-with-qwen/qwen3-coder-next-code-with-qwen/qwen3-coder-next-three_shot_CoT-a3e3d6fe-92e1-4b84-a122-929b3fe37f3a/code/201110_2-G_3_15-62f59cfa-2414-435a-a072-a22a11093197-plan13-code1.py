from z3 import *

# Rider indices: 0-Reynaldo, 1-Seamus, 2-Theresa, 3-Yuki
# Bicycle indices: 0-F, 1-G, 2-H, 3-J

# Assignment variables
r1 = [[Bool(f"r1_{i}_{j}") for j in range(4)] for i in range(4)]
r2 = [[Bool(f"r2_{i}_{j}") for j in range(4)] for i in range(4)]

solver = Solver()

# Day 1 assignment constraints
## Each rider tests exactly one bicycle on day 1
for i in range(4):
    solver.add(AtMost(*[r1[i][j] for j in range(4)], 1))
    solver.add(AtLeast(*[r1[i][j] for j in range(4)], 1))

## Each bicycle is tested by exactly one rider on day 1
for j in range(4):
    solver.add(AtMost(*[r1[i][j] for i in range(4)], 1))
    solver.add(AtLeast(*[r1[i][j] for i in range(4)], 1))

# Day 2 assignment constraints
## Each rider tests exactly one bicycle on day 2
for i in range(4):
    solver.add(AtMost(*[r2[i][j] for j in range(4)], 1))
    solver.add(AtLeast(*[r2[i][j] for j in range(4)], 1))

## Each bicycle is tested by exactly one rider on day 2
for j in range(4):
    solver.add(AtMost(*[r2[i][j] for i in range(4)], 1))
    solver.add(AtLeast(*[r2[i][j] for i in range(4)], 1))

# Prohibition constraints
## Reynaldo cannot test F (index 0)
solver.add(Not(r1[0][0]), Not(r2[0][0]))

## Yuki cannot test J (index 3)
solver.add(Not(r1[3][3]), Not(r2[3][3]))

# Theresa must test H (index 2) on at least one day
solver.add(Or(r1[2][2], r2[2][2]))

# Yuki-Seamus dependency: the bicycle Yuki tests on day 1 must be tested by Seamus on day 2
for j in range(4):
    solver.add(Implies(r1[3][j], r2[1][j]))

# Answer choices
answer_choices = [
    ("Reynaldo tests J on day 1", r1[0][3]),
    ("Reynaldo tests J on day 2", r2[0][3]),
    ("Seamus tests H on day 1", r1[1][2]),
    ("Yuki tests H on day 1", r1[3][2]),
    ("Yuki tests H on day 2", r2[3][2])
]

# Check each answer choice
answer_index_list = []
for idx, (desc, condition) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert the specific condition for that choice
    s_chk.add(condition)
    
    # If UNSAT, this choice cannot be true (EXCEPT answer)
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)