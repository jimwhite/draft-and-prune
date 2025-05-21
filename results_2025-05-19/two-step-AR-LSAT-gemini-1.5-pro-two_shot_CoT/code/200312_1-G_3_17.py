from z3 import *

# Variables
schedule = [[Int(f"schedule[{c}][{b}]") for b in range(3)] for c in range(3)]
c = Int('c')
b = Int('b')
b1 = Int('b1')
b2 = Int('b2')

# Solver
solver = Solver()

# Constraint 1: Domain
solver.add(ForAll([c, b], Implies(And(c >= 0, c <= 2, b >= 0, b <= 2), And(schedule[c][b] >= 0, schedule[c][b] <= 4))))

# Constraint 2: No two batches of same cookie on same day
solver.add(ForAll([c, b1, b2], Implies(And(c >= 0, c <= 2, b1 >= 0, b1 <= 2, b2 >= 0, b2 <= 2, b1 != b2), schedule[c][b1] != schedule[c][b2])))

# Constraint 3: At least one batch on Monday
solver.add(Or([Or([schedule[c][b] == 0 for b in range(3)]) for c in range(3)]))

# Constraint 4: Oatmeal 2nd batch and Peanut Butter 1st batch on same day
solver.add(schedule[0][1] == schedule[1][0])

# Constraint 5: Sugar 2nd batch on Thursday
solver.add(schedule[2][1] == 3)

# Constraint 6: Exactly one batch on Friday
solver.add(Sum([If(schedule[c][b] == 4, 1, 0) for c in range(3) for b in range(3)]) == 1)

# Check answer choices
options = [
    (0, "schedule[2][0] == 0"),  # A
    (1, "schedule[0][0] == 1"),  # B
    (2, "schedule[0][2] == 4"),  # C
    (3, "schedule[1][0] == 2"),  # D
    (4, "schedule[1][1] == 1")   # E
]

for i, option_str in options:
    solver.push()
    solver.add(eval(option_str))
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()
