from z3 import *

# Variables
schedule = [[Int(f'schedule[{c}][{b}]') for b in range(3)] for c in range(3)]

# Solver
solver = Solver()

# Constraints
# Constraint 1 (Domain of schedule)
solver.add(And([And(schedule[c][b] >= 0, schedule[c][b] <= 4) for c in range(3) for b in range(3)]))
# Constraint 2 (No two batches of same cookie on same day)
solver.add(And([Distinct(schedule[c]) for c in range(3)]))
# Constraint 3 (At least one batch on Monday)
solver.add(Or([schedule[c][b] == 0 for c in range(3) for b in range(3)]))
# Constraint 4 (Oatmeal 2nd batch and Peanut Butter 1st batch on same day)
solver.add(schedule[0][1] == schedule[1][0])
# Constraint 5 (Sugar 2nd batch on Thursday)
solver.add(schedule[2][1] == 3)
# Constraint 6 (Exactly one batch on Friday)
solver.add(Sum([If(schedule[c][b] == 4, 1, 0) for c in range(3) for b in range(3)]) == 1)

# Answer choices
choices = [
    (2, 0, 0),  # A: Sugar 1st on Monday
    (0, 0, 1),  # B: Oatmeal 1st on Tuesday
    (0, 2, 4),  # C: Oatmeal 3rd on Friday
    (1, 0, 2),  # D: Peanut Butter 1st on Wednesday
    (1, 1, 1)   # E: Peanut Butter 2nd on Tuesday
]

for i, (c, b, d) in enumerate(choices):
    solver.push()
    solver.add(schedule[c][b] == d)
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()
