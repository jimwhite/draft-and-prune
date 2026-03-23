from z3 import *

# Rider indices: 0-Reynaldo, 1-Seamus, 2-Theresa, 3-Yuki
# Bicycle indices: 0-F, 1-G, 2-H, 3-J

# r1[i][b] = True if rider i tests bicycle b on day 1
r1 = [[Bool(f"r1_{i}_{b}") for b in range(4)] for i in range(4)]
# r2[i][b] = True if rider i tests bicycle b on day 2
r2 = [[Bool(f"r2_{i}_{b}") for b in range(4)] for i in range(4)]

solver = Solver()

# Day 1 assignment constraints
## Each rider tests exactly one bicycle on day 1
for i in range(4):
    solver.add(Pb([(r1[i][b], 1) for b in range(4)], 1))

## Each bicycle is tested by exactly one rider on day 1
for b in range(4):
    solver.add(Pb([(r1[i][b], 1) for i in range(4)], 1))

# Day 2 assignment constraints
## Each rider tests exactly one bicycle on day 2
for i in range(4):
    solver.add(Pb([(r2[i][b], 1) for b in range(4)], 1))

## Each bicycle is tested by exactly one rider on day 2
for b in range(4):
    solver.add(Pb([(r2[i][b], 1) for i in range(4)], 1))

# Forbidden constraints
## Reynaldo cannot test F on either day
solver.add(Not(r1[0][0]), Not(r2[0][0]))

## Yuki cannot test J on either day
solver.add(Not(r1[3][3]), Not(r2[3][3]))

# Theresa must test H on at least one day
solver.add(Or(r1[2][2], r2[2][2]))

# Yuki-Seamus dependency: The bicycle Yuki tests on day 1 must be tested by Seamus on day 2
for b in range(4):
    solver.add(Implies(r1[3][b], r2[1][b]))

# Answer choices: each is "Both X and Y test J" meaning they both test bicycle J on the same day
# Choices indices: 0-Both Reynaldo and Seamus test J, 1-Both Reynaldo and Theresa test J,
#                 2-Both Reynaldo and Yuki test G, 3-Both Seamus and Theresa test G,
#                 4-Both Theresa and Yuki test F
answer_choices = [
    (0, 1, 3),  # Reynaldo and Seamus test J: (r1[0][3] and r1[1][3]) or (r2[0][3] and r2[1][3])
    (0, 2, 3),  # Reynaldo and Theresa test J: (r1[0][3] and r1[2][3]) or (r2[0][3] and r2[2][3])
    (0, 3, 1),  # Reynaldo and Yuki test G: (r1[0][1] and r1[3][1]) or (r2[0][1] and r2[3][1])
    (1, 2, 1),  # Seamus and Theresa test G: (r1[1][1] and r1[2][1]) or (r2[1][1] and r2[2][1])
    (2, 3, 0)   # Theresa and Yuki test F: (r1[2][0] and r1[3][0]) or (r2[2][0] and r2[3][0])
]

answer_index_list = []
for idx, (rider1, rider2, bike) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add constraint: both riders test the same bicycle on the same day
    s_chk.add(Or(
        And(r1[rider1][bike], r1[rider2][bike]),
        And(r2[rider1][bike], r2[rider2][bike])
    ))
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)