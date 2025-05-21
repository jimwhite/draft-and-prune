from z3 import *

# Variables
assignment = Array('assignment', IntSort(), IntSort())
days = 2
riders = 4
bikes = 4

# Solver
solver = Solver()

# Constraints
for d in range(days):
    for r in range(riders):
        solver.add(assignment[d][r] >= 0, assignment[d][r] < bikes)

for d in range(days):
    solver.add(Distinct([assignment[d][r] for r in range(riders)]))

for r in range(riders):
    solver.add(Distinct([assignment[d][r] for d in range(days)]))

for d in range(days):
    solver.add(assignment[d][0] != 0)

for d in range(days):
    solver.add(assignment[d][3] != 3)

solver.add(Or(assignment[0][2] == 2, assignment[1][2] == 2))
solver.add(assignment[0][3] == assignment[1][1])

# Answer choices
options = [
    (1, 0, 1),  # Reynaldo tests G on the second day
    (0, 1, 0),  # Seamus tests F on the first day
    (1, 2, 0),  # Theresa tests F on the second day
    (0, 0, 2),  # Reynaldo tests H on the first day
    (1, 3, 0)   # Yuki tests F on the second day
]

for i, (day, rider, bike) in enumerate(options):
    solver.push()
    solver.add(assignment[day][rider] == bike)
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()

