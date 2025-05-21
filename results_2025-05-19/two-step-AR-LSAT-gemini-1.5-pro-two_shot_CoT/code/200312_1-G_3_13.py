from z3 import *

# Variables
schedule = Array('schedule', IntSort(), IntSort(), IntSort())

# Solver
solver = Solver()

# Constraints
# Constraint 1 (Domain)
for c in range(3):
    for b in range(3):
        solver.add(schedule[c][b] >= 0, schedule[c][b] <= 4)

# Constraint 2 (No two batches of the same kind on the same day)
for c in range(3):
    for b1 in range(3):
        for b2 in range(b1 + 1, 3):
            solver.add(Implies(b1 != b2, schedule[c][b1] != schedule[c][b2]))

# Constraint 3 (At least one batch on Monday)
solver.add(Or([schedule[c][b] == 0 for c in range(3) for b in range(3)]))

# Constraint 4 (Oatmeal 2nd batch and Peanut Butter 1st batch on same day)
solver.add(schedule[0][1] == schedule[1][0])

# Constraint 5 (Sugar 2nd batch on Thursday)
solver.add(schedule[2][1] == 3)

# Constraint 6 (Three batches of each cookie)
for c in range(3):
    solver.add(Distinct([schedule[c][b] for b in range(3)]))


# Answer Choices
options = [
    [[0, 2, 3], [2, 3, 4], [0, 3, 4]],  # A
    [[0, 1, 3], [1, 2, 3], [0, 2, 3]],  # B
    [[1, 2, 3], [2, 3, 4], [1, 3, 4]],  # C
    [[0, 1, 3], [0, 2, 3], [0, 3, 4]],  # D
    [[0, 3, 4], [1, 2, 3], [0, 3, 4]]   # E
]

for i, option in enumerate(options):
    solver.push()
    for c in range(3):
        for b in range(3):
            solver.add(schedule[c][b] == option[c][b])
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()
