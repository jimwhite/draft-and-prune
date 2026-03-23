from z3 import *

# Riders: 0-Reynaldo, 1-Seamus, 2-Theresa, 3-Yuki
# Bicycles: 0-F, 1-G, 2-H, 3-J

# Variables
first = [[Bool(f"first_{i}_{j}") for j in range(4)] for i in range(4)]
second = [[Bool(f"second_{i}_{j}") for j in range(4)] for i in range(4)]

solver = Solver()

# Day 1 assignment constraints
for i in range(4):
    solver.add(PbAtLeast(*[(first[i][j], 1) for j in range(4)], 1))
    solver.add(PbAtMost(*[(first[i][j], 1) for j in range(4)], 1))
for j in range(4):
    solver.add(PbAtLeast(*[(first[i][j], 1) for i in range(4)], 1))
    solver.add(PbAtMost(*[(first[i][j], 1) for i in range(4)], 1))

# Day 2 assignment constraints
for i in range(4):
    solver.add(PbAtLeast(*[(second[i][j], 1) for j in range(4)], 1))
    solver.add(PbAtMost(*[(second[i][j], 1) for j in range(4)], 1))
for j in range(4):
    solver.add(PbAtLeast(*[(second[i][j], 1) for i in range(4)], 1))
    solver.add(PbAtMost(*[(second[i][j], 1) for i in range(4)], 1))

# Basic restriction constraints
# Reynaldo cannot test F (index 0) on either day
solver.add(Not(first[0][0]))
solver.add(Not(second[0][0]))

# Yuki cannot test J (index 3) on either day
solver.add(Not(first[3][3]))
solver.add(Not(second[3][3]))

# Theresa must test H (index 2) on some day
solver.add(Or(first[2][2], second[2][2]))

# Yuki-Seamus linkage: the bicycle Yuki tests on day 1 must be exactly the one Seamus tests on day 2
for j in range(4):
    solver.add(first[3][j] == second[1][j])

# Answer choices
answer_choices = [
    first[0][3],      # Choice 0: Reynaldo tests J on the first day
    second[0][3],     # Choice 1: Reynaldo tests J on the second day
    first[1][2],      # Choice 2: Seamus tests H on the first day
    first[3][2],      # Choice 3: Yuki tests H on the first day
    second[3][2]      # Choice 4: Yuki tests H on the second day
]

# Check each answer choice
answer_index_list = []
for idx, cond in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(cond)
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)