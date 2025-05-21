from z3 import *

# Define variables
schedule = Array('schedule', IntSort(), IntSort(), IntSort())

# Define solver
solver = Solver()

# Constraint 1: Domain (Corrected: Use nested loops instead of generator expression within ForAll)
for c in range(3):
    for b in range(3):
        solver.add(And(schedule[c][b] >= 0, schedule[c][b] <= 4))

# Constraint 2: No two batches of the same kind on the same day
for c in range(3):
    for b1 in range(3):
        for b2 in range(3):
            if b1 != b2:  # Simplified the Implies to an if condition
                solver.add(schedule[c][b1] != schedule[c][b2])

# Constraint 3: At least one batch on Monday
solver.add(Or([Or([schedule[c][b] == 0 for b in range(3)]) for c in range(3)]))

# Constraint 4: Oatmeal 2nd batch and Peanut Butter 1st batch on same day
solver.add(schedule[0][1] == schedule[1][0])

# Constraint 5: Sugar 2nd batch on Thursday
solver.add(schedule[2][1] == 3)

# Constraint 6: Peanut Butter 1st batch on Tuesday
solver.add(schedule[1][0] == 1)

# Answer choices
choices = [
    Or([And(schedule[c1][0] == 0, schedule[c2][0] == 0) for c1 in range(3) for c2 in range(3) if c1 != c2]),
    Or([And(schedule[c1][0] == 1, schedule[c2][0] == 1) for c1 in range(3) for c2 in range(3) if c1 != c2]),
    Or([And(schedule[c1][1] == 2, schedule[c2][1] == 2) for c1 in range(3) for c2 in range(3) if c1 != c2]),
    Or([And(schedule[c1][1] == 3, schedule[c2][1] == 3) for c1 in range(3) for c2 in range(3) if c1 != c2]),
    Or([And(schedule[c1][2] == 4, schedule[c2][2] == 4) for c1 in range(3) for c2 in range(3) if c1 != c2])
]

for i, choice in enumerate(choices):
    solver.push()
    solver.add(choice)
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()
