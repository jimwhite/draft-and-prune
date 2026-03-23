from z3 import *

# Rider indices: 0-Reynaldo, 1-Seamus, 2-Theresa, 3-Yuki
# Bicycle indices: 0-F, 1-G, 2-H, 3-J

# Day 1 assignment variables: d1[r][b] = True if rider r tests bicycle b on day 1
d1 = [[Bool(f"d1_{r}_{b}") for b in range(4)] for r in range(4)]

# Day 2 assignment variables: d2[r][b] = True if rider r tests bicycle b on day 2
d2 = [[Bool(f"d2_{r}_{b}") for b in range(4)] for r in range(4)]

# Base solver
solver = Solver()

# Day 1 constraints: each rider tests exactly one bicycle, each bicycle tested by exactly one rider
for r in range(4):
    solver.add(Sum([If(d1[r][b], 1, 0) for b in range(4)]) == 1)
for b in range(4):
    solver.add(Sum([If(d1[r][b], 1, 0) for r in range(4)]) == 1)

# Day 2 constraints: each rider tests exactly one bicycle, each bicycle tested by exactly one rider
for r in range(4):
    solver.add(Sum([If(d2[r][b], 1, 0) for b in range(4)]) == 1)
for b in range(4):
    solver.add(Sum([If(d2[r][b], 1, 0) for r in range(4)]) == 1)

# Problem-specific constraints
# Reynaldo cannot test F on either day
solver.add(Not(d1[0][0]), Not(d2[0][0]))

# Yuki cannot test J on either day
solver.add(Not(d1[3][3]), Not(d2[3][3]))

# Theresa must test H on at least one day
solver.add(Or(d1[2][2], d2[2][2]))

# The bicycle Yuki tests on day 1 must be tested by Seamus on day 2
for b in range(4):
    solver.add(Implies(d1[3][b], d2[1][b]))

# Answer choices (as logical conditions)
# 0: Both Reynaldo and Seamus test J
#    (d1[0][3] or d2[0][3]) and (d1[1][3] or d2[1][3])
# 1: Both Reynaldo and Theresa test J
#    (d1[0][3] or d2[0][3]) and (d1[2][3] or d2[2][3])
# 2: Both Reynaldo and Yuki test G
#    (d1[0][1] or d2[0][1]) and (d1[3][1] or d2[3][1])
# 3: Both Seamus and Theresa test G
#    (d1[1][1] or d2[1][1]) and (d1[2][1] or d2[2][1])
# 4: Both Theresa and Yuki test F
#    (d1[2][0] or d2[2][0]) and (d1[3][0] or d2[3][0])

answer_choices = [
    lambda: Or(Or(d1[0][3], d2[0][3]), And(d1[1][3], d2[1][3])),
    lambda: Or(Or(d1[0][3], d2[0][3]), And(d1[2][3], d2[2][3])),
    lambda: Or(Or(d1[0][1], d2[0][1]), And(d1[3][1], d2[3][1])),
    lambda: Or(Or(d1[1][1], d2[1][1]), And(d1[2][1], d2[2][1])),
    lambda: Or(Or(d1[2][0], d2[2][0]), And(d1[3][0], d2[3][0]))
]

# Actually, let's be more precise: each choice means both riders test the same bicycle
# For choice i, we need to check if it's possible for both riders to test the specified bicycle (at least once each, possibly on different days)
# But note: for a given bicycle b, only one rider can test it per day. So if both riders test the same bicycle, they must do so on different days.

# Let's re-encode each choice properly:
def get_choice_constraint(choice_idx):
    if choice_idx == 0:  # Both Reynaldo and Seamus test J (bicycle 3)
        return And(
            Or(d1[0][3], d2[0][3]),
            Or(d1[1][3], d2[1][3])
        )
    elif choice_idx == 1:  # Both Reynaldo and Theresa test J (bicycle 3)
        return And(
            Or(d1[0][3], d2[0][3]),
            Or(d1[2][3], d2[2][3])
        )
    elif choice_idx == 2:  # Both Reynaldo and Yuki test G (bicycle 1)
        return And(
            Or(d1[0][1], d2[0][1]),
            Or(d1[3][1], d2[3][1])
        )
    elif choice_idx == 3:  # Both Seamus and Theresa test G (bicycle 1)
        return And(
            Or(d1[1][1], d2[1][1]),
            Or(d1[2][1], d2[2][1])
        )
    elif choice_idx == 4:  # Both Theresa and Yuki test F (bicycle 0)
        return And(
            Or(d1[2][0], d2[2][0]),
            Or(d1[3][0], d2[3][0])
        )

answer_index_list = []
for idx in range(5):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add constraint for the choice
    s_chk.add(get_choice_constraint(idx))
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)