from z3 import *

# Rider indices: 0-Reynaldo, 1-Seamus, 2-Theresa, 3-Yuki
# Bicycle indices: 0-F, 1-G, 2-H, 3-J

day1 = [[Bool(f"day1_{r}_{b}") for b in range(4)] for r in range(4)]
day2 = [[Bool(f"day2_{r}_{b}") for b in range(4)] for r in range(4)]

solver = Solver()

# Bijective constraints for day 1
for r in range(4):
    solver.add(Or([day1[r][b] for b in range(4)]))
for b in range(4):
    solver.add(Or([day1[r][b] for r in range(4)]))
for r in range(4):
    for b1 in range(4):
        for b2 in range(b1 + 1, 4):
            solver.add(Not(day1[r][b1], day1[r][b2]))
for b in range(4):
    for r1 in range(4):
        for r2 in range(r1 + 1, 4):
            solver.add(Not(day1[r1][b], day1[r2][b]))

# Bijective constraints for day 2
for r in range(4):
    solver.add(Or([day2[r][b] for b in range(4)]))
for b in range(4):
    solver.add(Or([day2[r][b] for r in range(4)]))
for r in range(4):
    for b1 in range(4):
        for b2 in range(b1 + 1, 4):
            solver.add(Not(day2[r][b1], day2[r][b2]))
for b in range(4):
    for r1 in range(4):
        for r2 in range(r1 + 1, 4):
            solver.add(Not(day2[r1][b], day2[r2][b]))

# Explicit constraints
# Reynaldo cannot test F on either day
solver.add(Not(day1[0][0]), Not(day2[0][0]))

# Yuki cannot test J on either day
solver.add(Not(day1[3][3]), Not(day2[3][3]))

# Theresa must test H on at least one day
solver.add(Or(day1[2][2], day2[2][2]))

# The bicycle Yuki tests on day 1 must be tested by Seamus on day 2
for b in range(4):
    solver.add(Implies(day1[3][b], day2[1][b]))

# Answer choices: each choice is a pair of riders and bicycle J
# "Both X and Y test J" means: (day1[X][J] and day2[Y][J]) OR (day1[Y][J] and day2[X][J])
answer_choices = [
    ((0, 1), 3),   # Both Reynaldo and Seamus test J
    ((0, 2), 3),   # Both Reynaldo and Theresa test J
    ((0, 3), 1),   # Both Reynaldo and Yuki test G
    ((1, 2), 1),   # Both Seamus and Theresa test G
    ((2, 3), 0)    # Both Theresa and Yuki test F
]

forbidden_choice_indices = []

for idx, ((r1, r2), b) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add condition: (day1[r1][b] and day2[r2][b]) or (day1[r2][b] and day2[r1][b])
    s_chk.add(Or(
        And(day1[r1][b], day2[r2][b]),
        And(day1[r2][b], day2[r1][b])
    ))
    
    if s_chk.check() == unsat:
        forbidden_choice_indices.append(idx)

print(forbidden_choice_indices)