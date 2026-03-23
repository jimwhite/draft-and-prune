from z3 import *

# Rider indices: 0-Reynaldo, 1-Seamus, 2-Theresa, 3-Yuki
# Bicycle indices: 0-F, 1-G, 2-H, 3-J

# r1[i][j] = True if rider i tests bicycle j on day 1
r1 = [[Bool(f"r1_{i}_{j}") for j in range(4)] for i in range(4)]
# r2[i][j] = True if rider i tests bicycle j on day 2
r2 = [[Bool(f"r2_{i}_{j}") for j in range(4)] for i in range(4)]

solver = Solver()

# Day 1 assignment constraints
for i in range(4):
    solver.add(Sum([If(r1[i][j], 1, 0) for j in range(4)]) == 1)
for j in range(4):
    solver.add(Sum([If(r1[i][j], 1, 0) for i in range(4)]) == 1)

# Day 2 assignment constraints
for i in range(4):
    solver.add(Sum([If(r2[i][j], 1, 0) for j in range(4)]) == 1)
for j in range(4):
    solver.add(Sum([If(r2[i][j], 1, 0) for i in range(4)]) == 1)

# Exclusivity constraints
# Reynaldo cannot test F on either day (rider 0, bicycle 0)
solver.add(Not(r1[0][0]), Not(r2[0][0]))

# Yuki cannot test J on either day (rider 3, bicycle 3)
solver.add(Not(r1[3][3]), Not(r2[3][3]))

# Theresa must test H on some day (rider 2, bicycle 2)
solver.add(Or(r1[2][2], r2[2][2]))

# Cross-day dependency: Yuki's day 1 bicycle must be tested by Seamus on day 2
for j in range(4):
    solver.add(Implies(r1[3][j], r2[1][j]))

# Answer choices
answer_choices = [
    ("Reynaldo tests J on day 1", r1[0][3]),      # A
    ("Reynaldo tests J on day 2", r2[0][3]),      # B
    ("Seamus tests H on day 1", r1[1][2]),        # C
    ("Yuki tests H on day 1", r1[3][2]),          # D
    ("Yuki tests H on day 2", r2[3][2])           # E
]

# Check each answer choice for consistency
impossible_index_list = []
for idx, (desc, condition) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add the specific condition for this choice
    s_chk.add(condition)
    
    if s_chk.check() == unsat:
        impossible_index_list.append(idx)

print(impossible_index_list)