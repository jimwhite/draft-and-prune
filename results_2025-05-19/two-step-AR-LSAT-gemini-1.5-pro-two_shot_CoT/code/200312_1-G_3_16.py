from z3 import *

# Variables
schedule = Array('schedule', IntSort(), IntSort())

# Solver
solver = Solver()

# Constraints
for c in range(3):
    for b in range(3):
        solver.add(schedule[c][b] >= 0, schedule[c][b] < 5)

for c in range(3):
    for b1 in range(3):
        for b2 in range(3):
            if b1 != b2:
                solver.add(schedule[c][b1] != schedule[c][b2])

# At least one cell must be 0
solver.add(Or([And(c >= 0, c < 3, b >= 0, b < 3, schedule[c][b] == 0) for c in range(3) for b in range(3)]))

solver.add(schedule[0][1] == schedule[1][0])

solver.add(schedule[2][1] == 3)

for c in range(3):
    for b in range(3):
        solver.add(schedule[c][b] != 2)


# Answer choices
options = [
    Or(sum([If(schedule[c][b] == 1, 1, 0) for c in range(3) for b in range(3)]) != 3, Exists([Int('d')], And(Int('d') >= 0, Int('d') < 5, Int('d') != 1, sum([If(schedule[c][b] == Int('d'), 1, 0) for c in range(3) for b in range(3)]) == 3))),
    Or(sum([If(schedule[c][b] == 4, 1, 0) for c in range(3) for b in range(3)]) != 3, Exists([Int('d')], And(Int('d') >= 0, Int('d') < 5, Int('d') != 4, sum([If(schedule[c][b] == Int('d'), 1, 0) for c in range(3) for b in range(3)]) == 3))),
    sum([If(schedule[c][b] == 0, 1, 0) for c in range(3) for b in range(3)]) < 2,
    sum([If(schedule[c][b] == 3, 1, 0) for c in range(3) for b in range(3)]) < 2,
    sum([If(schedule[c][b] == 0, 1, 0) for c in range(3) for b in range(3)]) >= sum([If(schedule[c][b] == 1, 1, 0) for c in range(3) for b in range(3)])
]

for i, option in enumerate(options):
    solver.push()
    solver.add(option)
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()

