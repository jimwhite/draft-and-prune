from z3 import *

# Define variables
assignment = Array('assignment', IntSort(), IntSort())
rider = Int('rider')
day = Int('day')

# Define solver
solver = Solver()

# Constraint 1: Domain
solver.add(ForAll([rider, day], Implies(And(rider >= 0, rider < 4, day >= 0, day < 2), And(assignment[rider][day] >= 0, assignment[rider][day] < 4))))

# Constraint 2: Each rider tests a different bike each day
rider = Int('rider')
solver.add(ForAll([rider], Implies(And(rider >= 0, rider < 4), Distinct([assignment[rider][0], assignment[rider][1]]))))

# Constraint 3: All bikes are tested each day
day = Int('day')
solver.add(ForAll([day], Implies(And(day >= 0, day < 2), Distinct([assignment[0][day], assignment[1][day], assignment[2][day], assignment[3][day]]))))

# Constraint 4: Reynaldo cannot test F
day = Int('day')
solver.add(ForAll([day], Implies(And(day >= 0, day < 2), assignment[0][day] != 0)))

# Constraint 5: Yuki cannot test J
day = Int('day')
solver.add(ForAll([day], Implies(And(day >= 0, day < 2), assignment[3][day] != 3)))

# Constraint 6: Theresa must test H
solver.add(Or(assignment[2][0] == 2, assignment[2][1] == 2))

# Constraint 7: Yuki's day 1 bike is Seamus's day 2 bike
solver.add(assignment[1][1] == assignment[3][0])

# Question condition: Theresa tests G on day 2
solver.add(assignment[2][1] == 1)

# Answer choices
options = [
    (0, 0, 2),  # Reynaldo tests H on the first day
    (0, 0, 3),  # Reynaldo tests J on the first day
    (2, 1, 2),  # Theresa tests H on the second day
    (2, 0, 3),  # Theresa tests J on the first day
    (3, 1, 2)   # Yuki tests H on the second day
]

for i, option in enumerate(options):
    solver.push()
    solver.add(assignment[option[0]][option[1]] != option[2])
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()

