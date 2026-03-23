from z3 import *

# Rider indices: 0-Reynaldo, 1-Seamus, 2-Theresa, 3-Yuki
# Bicycle indices: 0-F, 1-G, 2-H, 3-J

day1 = [[Bool(f"day1_{r}_{b}") for b in range(4)] for r in range(4)]
day2 = [[Bool(f"day2_{r}_{b}") for b in range(4)] for r in range(4)]

solver = Solver()

# Day 1 constraints: each rider tests exactly one bike, each bike tested by exactly one rider
for r in range(4):
    solver.add(AtMost(*[day1[r][b] for b in range(4)], 1))
    solver.add(AtLeast(*[day1[r][b] for b in range(4)], 1))
for b in range(4):
    solver.add(AtMost(*[day1[r][b] for r in range(4)], 1))
    solver.add(AtLeast(*[day1[r][b] for r in range(4)], 1))

# Day 2 constraints: each rider tests exactly one bike, each bike tested by exactly one rider
for r in range(4):
    solver.add(AtMost(*[day2[r][b] for b in range(4)], 1))
    solver.add(AtLeast(*[day2[r][b] for b in range(4)], 1))
for b in range(4):
    solver.add(AtMost(*[day2[r][b] for r in range(4)], 1))
    solver.add(AtLeast(*[day2[r][b] for r in range(4)], 1))

# Exclusion constraints
solver.add(Not(day1[0][0]))  # Reynaldo cannot test F (index 0)
solver.add(Not(day1[3][3]))  # Yuki cannot test J (index 3)

# Theresa must test H on some day
solver.add(Or(day1[2][2], day2[2][2]))

# Yuki-Seamus linking constraint: the bike Yuki tests on day1 must be the same bike Seamus tests on day2
for b in range(4):
    solver.add(day1[3][b] == day2[1][b])

# Answer choices (each is a pair of riders and a bicycle)
answer_choices = [
    ("Both Reynaldo and Seamus test J.", 0, 1, 3),   # Reynaldo (0) and Seamus (1) test J (3)
    ("Both Reynaldo and Theresa test J.", 0, 2, 3),  # Reynaldo (0) and Theresa (2) test J (3)
    ("Both Reynaldo and Yuki test G.", 0, 3, 1),     # Reynaldo (0) and Yuki (3) test G (1)
    ("Both Seamus and Theresa test G.", 1, 2, 1),    # Seamus (1) and Theresa (2) test G (1)
    ("Both Theresa and Yuki test F.", 2, 3, 0)       # Theresa (2) and Yuki (3) test F (0)
]

answer_index_list = []
for idx, (_, r1, r2, b) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add constraint that both riders test the specified bicycle on day 1
    s_chk.add(day1[r1][b])
    s_chk.add(day1[r2][b])
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)