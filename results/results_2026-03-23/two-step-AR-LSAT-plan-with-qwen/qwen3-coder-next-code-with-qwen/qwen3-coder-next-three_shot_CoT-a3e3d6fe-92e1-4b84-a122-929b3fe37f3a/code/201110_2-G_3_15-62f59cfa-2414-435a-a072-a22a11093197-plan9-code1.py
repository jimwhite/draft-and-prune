from z3 import *

# Rider indices: 0-Reynaldo, 1-Seamus, 2-Theresa, 3-Yuki
# Bicycle indices: 0-F, 1-G, 2-H, 3-J

# Decision variables
first = [[Bool(f"first_{r}_{b}") for b in range(4)] for r in range(4)]
second = [[Bool(f"second_{r}_{b}") for b in range(4)] for r in range(4)]

solver = Solver()

# Day 1 assignment constraints
for r in range(4):
    solver.add(Sum([If(first[r][b], 1, 0) for b in range(4)]) == 1)
for b in range(4):
    solver.add(Sum([If(first[r][b], 1, 0) for r in range(4)]) == 1)

# Day 2 assignment constraints
for r in range(4):
    solver.add(Sum([If(second[r][b], 1, 0) for b in range(4)]) == 1)
for b in range(4):
    solver.add(Sum([If(second[r][b], 1, 0) for r in range(4)]) == 1)

# Problem-specific constraints
# Reynaldo cannot test F on either day (rider 0, bicycle 0)
solver.add(Not(first[0][0]), Not(second[0][0]))

# Yuki cannot test J on either day (rider 3, bicycle 3)
solver.add(Not(first[3][3]), Not(second[3][3]))

# Theresa must test H on at least one day (rider 2, bicycle 2)
solver.add(Or(first[2][2], second[2][2]))

# The bicycle Yuki tests on day 1 must be tested by Seamus on day 2
for b in range(4):
    solver.add(Implies(first[3][b], second[1][b]))

# Answer choices
answer_choices = [
    first[0][3],      # Choice 0: Reynaldo tests J on day 1
    second[0][3],     # Choice 1: Reynaldo tests J on day 2
    first[1][2],      # Choice 2: Seamus tests H on day 1
    first[3][2],      # Choice 3: Yuki tests H on day 1
    second[3][2]      # Choice 4: Yuki tests H on day 2
]

answer_index_list = []
for i in range(5):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(answer_choices[i])
    
    if s_chk.check() == unsat:
        answer_index_list.append(i)

print(answer_index_list)