from z3 import *

# Rider indices: 0-Reynaldo, 1-Seamus, 2-Theresa, 3-Yuki
# Bicycle indices: 0-F, 1-G, 2-H, 3-J

# Day 1 assignments: R1[i][j] = True if rider i tests bicycle j on day 1
R1 = [[Bool(f"R1_{i}_{j}") for j in range(4)] for i in range(4)]
# Day 2 assignments: R2[i][j] = True if rider i tests bicycle j on day 2
R2 = [[Bool(f"R2_{i}_{j}") for j in range(4)] for i in range(4)]

solver = Solver()

# Day 1 constraints: each rider tests exactly one bicycle, each bicycle tested by exactly one rider
for i in range(4):
    solver.add(PbAtLeast([(R1[i][j], 1) for j in range(4)], 1))
    solver.add(PbAtMost([(R1[i][j], 1) for j in range(4)], 1))
for j in range(4):
    solver.add(PbAtLeast([(R1[i][j], 1) for i in range(4)], 1))
    solver.add(PbAtMost([(R1[i][j], 1) for i in range(4)], 1))

# Day 2 constraints: each rider tests exactly one bicycle, each bicycle tested by exactly one rider
for i in range(4):
    solver.add(PbAtLeast([(R2[i][j], 1) for j in range(4)], 1))
    solver.add(PbAtMost([(R2[i][j], 1) for j in range(4)], 1))
for j in range(4):
    solver.add(PbAtLeast([(R2[i][j], 1) for i in range(4)], 1))
    solver.add(PbAtMost([(R2[i][j], 1) for i in range(4)], 1))

# No rider tests the same bicycle on both days
for i in range(4):
    for j in range(4):
        solver.add(Implies(R1[i][j], Not(R2[i][j])))

# Prohibited assignments
# Reynaldo cannot test F (bicycle 0)
solver.add(Not(R1[0][0]), Not(R2[0][0]))
# Yuki cannot test J (bicycle 3)
solver.add(Not(R1[3][3]), Not(R2[3][3]))

# Theresa must test H (bicycle 2) on at least one day
solver.add(Or(R1[2][2], R2[2][2]))

# Yuki's day 1 bicycle must be tested by Seamus on day 2
for j in range(4):
    solver.add(Implies(R1[3][j], R2[1][j]))

# Answer choices: each is "Both X and Y test J"
# 0: Both Reynaldo and Seamus test J
# 1: Both Reynaldo and Theresa test J
# 2: Both Reynaldo and Yuki test G
# 3: Both Seamus and Theresa test G
# 4: Both Theresa and Yuki test F

answer_index_list = []
choices = [
    (0, 1, 3),  # Reynaldo, Seamus test J
    (0, 2, 3),  # Reynaldo, Theresa test J
    (0, 3, 1),  # Reynaldo, Yuki test G
    (1, 2, 1),  # Seamus, Theresa test G
    (2, 3, 0)   # Theresa, Yuki test F
]

for idx, (rider1, rider2, bike) in enumerate(choices):
    # Check both day 1 and day 2 scenarios
    possible = False
    
    for day in [1, 2]:
        s_chk = Solver()
        s_chk.add(solver.assertions())
        
        if day == 1:
            s_chk.add(R1[rider1][bike], R1[rider2][bike])
        else:
            s_chk.add(R2[rider1][bike], R2[rider2][bike])
        
        if s_chk.check() == sat:
            possible = True
            break
    
    if not possible:
        answer_index_list.append(idx)

print(answer_index_list)