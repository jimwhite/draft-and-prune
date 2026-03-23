from z3 import *

# Rider indices: 0-Reynaldo, 1-Seamus, 2-Theresa, 3-Yuki
# Bicycle indices: 0-F, 1-G, 2-H, 3-J

# day1[r][b] = True if rider r tests bicycle b on day 1
day1 = [[Bool(f"day1_{r}_{b}") for b in range(4)] for r in range(4)]
# day2[r][b] = True if rider r tests bicycle b on day 2
day2 = [[Bool(f"day2_{r}_{b}") for b in range(4)] for r in range(4)]

solver = Solver()

# Day 1 assignment constraints
## Each rider tests exactly one bicycle on day 1
for r in range(4):
    solver.add(AtMost(*[day1[r][b] for b in range(4)], 1))
    solver.add(AtLeast(*[day1[r][b] for b in range(4)], 1))

## Each bicycle is tested by exactly one rider on day 1
for b in range(4):
    solver.add(AtMost(*[day1[r][b] for r in range(4)], 1))
    solver.add(AtLeast(*[day1[r][b] for r in range(4)], 1))

# Day 2 assignment constraints
## Each rider tests exactly one bicycle on day 2
for r in range(4):
    solver.add(AtMost(*[day2[r][b] for b in range(4)], 1))
    solver.add(AtLeast(*[day2[r][b] for b in range(4)], 1))

## Each bicycle is tested by exactly one rider on day 2
for b in range(4):
    solver.add(AtMost(*[day2[r][b] for r in range(4)], 1))
    solver.add(AtLeast(*[day2[r][b] for r in range(4)], 1))

# Hard constraints
## Reynaldo cannot test F on any day
solver.add(Not(day1[0][0]), Not(day2[0][0]))

## Yuki cannot test J on any day
solver.add(Not(day1[3][3]), Not(day2[3][3]))

## Theresa must test H on some day
solver.add(Or(day1[2][2], day2[2][2]))

## The bicycle Yuki tests on day 1 must be tested by Seamus on day 2
for b in range(4):
    solver.add(Implies(day1[3][b], day2[1][b]))

# Answer choices (each is a pair of riders and a bicycle they both test on the same day)
# 0: Both Reynaldo and Seamus test J. -> day1[0][3] and day1[1][3]
# 1: Both Reynaldo and Theresa test J. -> day1[0][3] and day1[2][3]
# 2: Both Reynaldo and Yuki test G. -> day1[0][1] and day1[3][1]
# 3: Both Seamus and Theresa test G. -> day1[1][1] and day1[2][1]
# 4: Both Theresa and Yuki test F. -> day1[2][0] and day1[3][0]

answer_choices = [
    (0, 3),  # Reynaldo and Seamus test J
    (0, 2),  # Reynaldo and Theresa test J
    (0, 1),  # Reynaldo and Yuki test G
    (1, 2),  # Seamus and Theresa test G
    (2, 0)   # Theresa and Yuki test F
]

# Check each answer choice
answer_index_list = []
for idx, (r1, b) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add constraint that both riders test the same bicycle on day 1
    s_chk.add(day1[0][b])  # Reynaldo tests bicycle b on day 1
    s_chk.add(day1[1][b]) if idx == 0 else None  # Seamus tests J on day 1
    s_chk.add(day1[2][b]) if idx == 1 else None  # Theresa tests J on day 1
    s_chk.add(day1[3][b]) if idx == 2 else None  # Yuki tests G on day 1
    s_chk.add(day1[2][b]) if idx == 3 else None  # Theresa tests G on day 1
    s_chk.add(day1[2][b]) if idx == 4 else None  # Theresa tests F on day 1
    s_chk.add(day1[3][b]) if idx == 4 else None  # Yuki tests F on day 1
    
    # For choices where both riders are not Reynaldo, we need to add the second rider constraint
    if idx == 0:  # Seamus and J
        s_chk.add(day1[1][3])
    elif idx == 1:  # Theresa and J
        s_chk.add(day1[2][3])
    elif idx == 2:  # Yuki and G
        s_chk.add(day1[3][1])
    elif idx == 3:  # Seamus and Theresa test G
        s_chk.add(day1[1][1])
        s_chk.add(day1[2][1])
    elif idx == 4:  # Theresa and Yuki test F
        s_chk.add(day1[2][0])
        s_chk.add(day1[3][0])
    
    # If UNSAT, this choice CANNOT be true
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)