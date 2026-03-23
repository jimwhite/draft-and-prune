from z3 import *

# Rider indices: 0-Reynaldo, 1-Seamus, 2-Theresa, 3-Yuki
# Bicycle indices: 0-F, 1-G, 2-H, 3-J

# Day 1 assignment: d1[r][b] = True if rider r tests bicycle b on day 1
d1 = [[Bool(f"d1_{r}_{b}") for b in range(4)] for r in range(4)]

# Day 2 assignment: d2[r][b] = True if rider r tests bicycle b on day 2
d2 = [[Bool(f"d2_{r}_{b}") for b in range(4)] for r in range(4)]

solver = Solver()

# Per-rider constraints: each rider tests exactly one bicycle per day
for r in range(4):
    solver.add(Sum([d1[r][b] for b in range(4)]) == 1)
    solver.add(Sum([d2[r][b] for b in range(4)]) == 1)

# Per-bicycle constraints: each bicycle is tested by exactly one rider per day
for b in range(4):
    solver.add(Sum([d1[r][b] for r in range(4)]) == 1)
    solver.add(Sum([d2[r][b] for r in range(4)]) == 1)

# Reynaldo cannot test F on day 1
solver.add(Not(d1[0][0]))

# Yuki cannot test J on day 1
solver.add(Not(d1[3][3]))

# Theresa must test H on at least one day
solver.add(Or(d1[2][2], d2[2][2]))

# Yuki's day-1 bike must be tested by Seamus on day 2
for b in range(4):
    solver.add(d1[3][b] == d2[1][b])

# No rider repeats the same bicycle on both days
for r in range(4):
    for b in range(4):
        solver.add(Implies(d1[r][b], Not(d2[r][b])))

# Answer choices conditions
answer_choices = [
    # 0: Both Reynaldo and Seamus test J (bicycle index 3)
    Or(And(d1[0][3], d2[1][3]), And(d1[1][3], d2[0][3])),
    # 1: Both Reynaldo and Theresa test J (bicycle index 3)
    Or(And(d1[0][3], d2[2][3]), And(d1[2][3], d2[0][3])),
    # 2: Both Reynaldo and Yuki test G (bicycle index 1)
    Or(And(d1[0][1], d2[3][1]), And(d1[3][1], d2[0][1])),
    # 3: Both Seamus and Theresa test G (bicycle index 1)
    Or(And(d1[1][1], d2[2][1]), And(d1[2][1], d2[1][1])),
    # 4: Both Theresa and Yuki test F (bicycle index 0)
    Or(And(d1[2][0], d2[3][0]), And(d1[3][0], d2[2][0]))
]

answer_index_list = []
for idx, cond in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(cond)
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)