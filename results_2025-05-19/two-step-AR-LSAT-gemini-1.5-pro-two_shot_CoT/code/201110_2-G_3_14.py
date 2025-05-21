from z3 import *

# Define variables
assignment = Array('assignment', IntSort(), IntSort(), IntSort())
day = Int('day')
rider = Int('rider')

# Define solver
solver = Solver()

# Constraint 1: Domain
solver.add(ForAll([day, rider], Implies(And(day >= 0, day < 2, rider >=0, rider < 4), And(assignment[day][rider] >= 0, assignment[day][rider] < 4))))

# Constraint 2: Unique Bicycle per Rider per Day
solver.add(ForAll([day], Implies(And(day >= 0, day < 2), Distinct([assignment[day][rider] for rider in range(4)]))))


# Constraint 4: Reynaldo cannot test F
solver.add(ForAll([day], Implies(And(day >= 0, day < 2), assignment[day][0] != 0)))

# Constraint 5: Yuki cannot test J
solver.add(ForAll([day], Implies(And(day >= 0, day < 2), assignment[day][3] != 3)))

# Constraint 6: Theresa must test H
solver.add(Or(assignment[0][2] == 2, assignment[1][2] == 2))

# Constraint 7: Yuki's Day 1 bike is Seamus's Day 2 bike
solver.add(assignment[1][1] == assignment[0][3])

# Constraint 8: Theresa tests G on Day 2
solver.add(assignment[1][2] == 1)

# Answer choices
options = [
    (0, 0, 2),  # Reynaldo tests H on the first day
    (0, 0, 3),  # Reynaldo tests J on the first day
    (1, 2, 2),  # Theresa tests H on the second day
    (0, 2, 3),  # Theresa tests J on the first day
    (1, 3, 2)   # Yuki tests H on the second day
]

for i, option in enumerate(options):
    solver.push()
    solver.add(assignment[option[0]][option[1]] != option[2])
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()
