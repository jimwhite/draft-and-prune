from z3 import *

# Variables
schedule = Array('schedule', IntSort(), IntSort(), IntSort())

# Solver
solver = Solver()

# Days (0-4), Cookie Types (0-2), Batches (0-2)
days = range(5)
cookie_types = range(3)
batches = range(3)

# Constraint 1: Domain
solver.add(ForAll([d, c], Implies(And(d >= 0, d <= 4, c >= 0, c <= 2), And(schedule[d][c] >= -1, schedule[d][c] <= 2))))

# Constraint 2: Exactly three batches of each cookie type
solver.add(ForAll([c], Implies(And(c >= 0, c <= 2), Exists([d1, d2, d3], And(Distinct(d1, d2, d3), d1 >=0, d1 <= 4, d2 >= 0, d2 <= 4, d3 >= 0, d3 <= 4, schedule[d1][c] == 0, schedule[d2][c] == 1, schedule[d3][c] == 2)))))

# Constraint 3: No two batches of the same kind on the same day
solver.add(ForAll([c, d1, d2], Implies(And(c >= 0, c <= 2, d1 != d2, d1 >= 0, d1 <= 4, d2 >= 0, d2 <= 4), Implies(And(schedule[d1][c] != -1, schedule[d2][c] != -1), schedule[d1][c] != schedule[d2][c]))))

# Constraint 4: At least one batch on Monday
solver.add(Exists([c], And(c >= 0, c <= 2, schedule[0][c] != -1)))

# Constraint 5: Oatmeal 2nd batch and Peanut Butter 1st batch on same day
solver.add(ForAll([d], Implies(And(d >= 0, d <= 4), schedule[d][0] == 1 == schedule[d][1] == 0)))


# Constraint 6: Sugar 2nd batch on Thursday
solver.add(schedule[3][2] == 1)

# Constraint 7: Peanut Butter 1st batch on Tuesday
solver.add(schedule[1][1] == 0)

# Constraint 8: Only one batch per kind per day
solver.add(ForAll([d, c1, c2], Implies(And(d >= 0, d <= 4, c1 != c2, c1 >= 0, c1 <= 2, c2 >= 0, c2 <= 2, schedule[d][c1] != -1, schedule[d][c2] != -1), False)))

# Check answer choices
choices = [
    Exists([c1, c2], And(c1 != c2, c1 >= 0, c1 <= 2, c2 >= 0, c2 <= 2, schedule[0][c1] == 0, schedule[0][c2] == 0)),
    Exists([c1, c2], And(c1 != c2, c1 >= 0, c1 <= 2, c2 >= 0, c2 <= 2, schedule[1][c1] == 0, schedule[1][c2] == 0)),
    Exists([c1, c2], And(c1 != c2, c1 >= 0, c1 <= 2, c2 >= 0, c2 <= 2, schedule[2][c1] == 1, schedule[2][c2] == 1)),
    Exists([c1, c2], And(c1 != c2, c1 >= 0, c1 <= 2, c2 >= 0, c2 <= 2, schedule[3][c1] == 1, schedule[3][c2] == 1)),
    Exists([c1, c2], And(c1 != c2, c1 >= 0, c1 <= 2, c2 >= 0, c2 <= 2, schedule[4][c1] == 2, schedule[4][c2] == 2)),
]

for i, choice in enumerate(choices):
    solver.push()
    solver.add(choice)
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()
