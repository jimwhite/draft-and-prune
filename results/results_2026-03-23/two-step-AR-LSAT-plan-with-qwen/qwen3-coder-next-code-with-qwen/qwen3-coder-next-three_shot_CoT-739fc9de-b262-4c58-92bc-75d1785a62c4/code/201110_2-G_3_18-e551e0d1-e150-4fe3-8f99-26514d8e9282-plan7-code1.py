from z3 import *

# Rider indices: 0-Reynaldo, 1-Seamus, 2-Theresa, 3-Yuki
# Bicycle indices: 0-F, 1-G, 2-H, 3-J

rider_bike_day = [[[Bool(f"rbd_{i}_{j}_{d}") for d in range(2)] for j in range(4)] for i in range(4)]

solver = Solver()

# Coverage constraints: each bicycle is tested by exactly one rider each day
for d in range(2):
    for j in range(4):
        solver.add(Sum([rider_bike_day[i][j][d] for i in range(4)]) == 1)

# Uniqueness constraints: each rider tests exactly one bicycle per day
for i in range(4):
    for d in range(2):
        solver.add(Sum([rider_bike_day[i][j][d] for j in range(4)]) == 1)

# No-repeat constraint across days: each rider tests different bicycles on day 0 and day 1
for i in range(4):
    for j in range(4):
        solver.add(Not(And(rider_bike_day[i][j][0], rider_bike_day[i][j][1])))

# Explicit condition constraints
# Reynaldo cannot test F (bicycle 0)
solver.add(Not(rider_bike_day[0][0][0]))
solver.add(Not(rider_bike_day[0][0][1]))

# Yuki cannot test J (bicycle 3)
solver.add(Not(rider_bike_day[3][3][0]))
solver.add(Not(rider_bike_day[3][3][1]))

# Theresa must be one of the testers for H (bicycle 2) on at least one day
solver.add(Or(rider_bike_day[2][2][0], rider_bike_day[2][2][1]))

# The bicycle Yuki tests on day 0 must be tested by Seamus on day 1
for j in range(4):
    solver.add(rider_bike_day[3][j][0] == rider_bike_day[1][j][1])

# Answer choices: each is a pair of riders who test the same bicycle (on possibly different days)
# We interpret "Both X and Y test J" as: X tests J on some day AND Y tests J on some day
# Since each bicycle is tested exactly once per day, this means they test it on different days

answer_choices = [
    ("Both Reynaldo and Seamus test J.", 0, 1, 3),   # Reynaldo (0) and Seamus (1) test J (3)
    ("Both Reynaldo and Theresa test J.", 0, 2, 3), # Reynaldo (0) and Theresa (2) test J (3)
    ("Both Reynaldo and Yuki test G.", 0, 3, 1),    # Reynaldo (0) and Yuki (3) test G (1)
    ("Both Seamus and Theresa test G.", 1, 2, 1),   # Seamus (1) and Theresa (2) test G (1)
    ("Both Theresa and Yuki test F.", 2, 3, 0)      # Theresa (2) and Yuki (3) test F (0)
]

answer_index_list = []

for idx, (_, r1, r2, b) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add constraint: rider r1 tests bicycle b on some day AND rider r2 tests bicycle b on some day
    s_chk.add(Or(rider_bike_day[r1][b][0], rider_bike_day[r1][b][1]))
    s_chk.add(Or(rider_bike_day[r2][b][0], rider_bike_day[r2][b][1]))
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)