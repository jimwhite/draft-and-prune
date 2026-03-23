from z3 import *

# Rider indices: 0-Reynaldo, 1-Seamus, 2-Theresa, 3-Yuki
# Bicycle indices: 0-F, 1-G, 2-H, 3-J

# Assignment variables
first = [[Bool(f"first_{r}_{b}") for b in range(4)] for r in range(4)]
second = [[Bool(f"second_{r}_{b}") for b in range(4)] for r in range(4)]

solver = Solver()

# Day 1 permutation constraints
for r in range(4):
    solver.add(Sum([If(first[r][b], 1, 0) for b in range(4)]) == 1)
for b in range(4):
    solver.add(Sum([If(first[r][b], 1, 0) for r in range(4)]) == 1)

# Day 2 permutation constraints
for r in range(4):
    solver.add(Sum([If(second[r][b], 1, 0) for b in range(4)]) == 1)
for b in range(4):
    solver.add(Sum([If(second[r][b], 1, 0) for r in range(4)]) == 1)

# Individual constraints
# Reynaldo cannot test F on either day
solver.add(Not(first[0][0]), Not(second[0][0]))

# Yuki cannot test J on either day
solver.add(Not(first[3][3]), Not(second[3][3]))

# Theresa must test H on at least one day
solver.add(Or(first[2][2], second[2][2]))

# Yuki-Seamus dependency: the bicycle Yuki tests on day 1 must be tested by Seamus on day 2
for b in range(4):
    solver.add(Implies(first[3][b], second[1][b]))

# Answer choices
answer_choices = [
    ("Reynaldo tests J on the first day.", first[0][3]),  # Reynaldo (0) tests J (3) on day 1
    ("Reynaldo tests J on the second day.", second[0][3]),  # Reynaldo (0) tests J (3) on day 2
    ("Seamus tests H on the first day.", first[1][2]),  # Seamus (1) tests H (2) on day 1
    ("Yuki tests H on the first day.", first[3][2]),  # Yuki (3) tests H (2) on day 1
    ("Yuki tests H on the second day.", second[3][2])  # Yuki (3) tests H (2) on day 2
]

# Check each answer choice
answer_index_list = []
for idx, (_, condition) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add the condition for this answer choice
    s_chk.add(condition)
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)