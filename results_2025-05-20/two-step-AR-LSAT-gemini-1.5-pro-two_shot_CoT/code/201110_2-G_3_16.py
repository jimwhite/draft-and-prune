from z3 import *

# Variables
assignment = Array('assignment', IntSort(), IntSort())

# Solver
solver = Solver()

# Constraints
rider = Int('rider')
day = Int('day')
solver.add(ForAll([rider, day], Implies(And(rider >= 0, rider < 4, day >= 0, day < 2), And(assignment[rider][day] >= 0, assignment[rider][day] < 4))))

rider = Int('rider')
solver.add(ForAll([rider], Implies(And(rider >= 0, rider < 4), Distinct([assignment[rider][0], assignment[rider][1]]))))

day = Int('day')
solver.add(ForAll([day], Implies(And(day >= 0, day < 2), Distinct([assignment[0][day], assignment[1][day], assignment[2][day], assignment[3][day]]))))

day = Int('day')
solver.add(ForAll([day], Implies(And(day >= 0, day < 2), assignment[0][day] != 0)))

day = Int('day')
solver.add(ForAll([day], Implies(And(day >= 0, day < 2), assignment[3][day] != 3)))


solver.add(Or(assignment[2][0] == 2, assignment[2][1] == 2))

solver.add(assignment[1][1] == assignment[3][0])

# Answer choices
choices = [
    (0, 1, 1),  # Reynaldo tests G on the second day
    (1, 0, 0),  # Seamus tests F on the first day
    (2, 1, 0),  # Theresa tests F on the second day
    (0, 0, 2),  # Reynaldo tests H on the first day
    (3, 1, 0)   # Yuki tests F on the second day
]

for i, (rider_index, day_index, bike_index) in enumerate(choices):
    solver.push()
    solver.add(assignment[rider_index][day_index] == bike_index)
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()
