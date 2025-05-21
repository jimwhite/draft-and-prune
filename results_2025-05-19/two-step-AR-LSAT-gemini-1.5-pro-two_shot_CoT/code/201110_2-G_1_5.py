from z3 import *

R, S, T, V, X, Y = 0, 1, 2, 3, 4, 5

assignment = Array('assignment', IntSort(), IntSort())

solver = Solver()

# Constraint 1: Distinct Assignments
solver.add(Distinct([assignment[i] for i in range(6)]))

# Constraint 2: Parking Space Range
i = Int('i') # Declare i as an integer variable for the quantifier
solver.add(ForAll([i], Implies(And(i >= 0, i < 6), And(assignment[i] >= 0, assignment[i] <= 5))))

# Constraint 3: Young > Togowa
solver.add(assignment[Y] > assignment[T])

# Constraint 4: Xu > Souza
solver.add(assignment[X] > assignment[S])

# Constraint 5: Robertson > Young
solver.add(assignment[R] > assignment[Y])

# Constraint 6: Robertson's Parking Space
solver.add(Or(assignment[R] == 0, assignment[R] == 1, assignment[R] == 2, assignment[R] == 3))

# Constraint 7: Young > Souza (Question Condition)
solver.add(assignment[Y] > assignment[S])

options = [
    (T, 0),  # Togowa is assigned parking space #1
    (Y, 1),  # Young is assigned parking space #2
    (R, 2),  # Robertson is assigned parking space #3
    (S, 2),  # Souza is assigned parking space #3
    (V, 3)   # Vaughn is assigned parking space #4
]

for i, (employee, space) in enumerate(options):
    solver.push()
    solver.add(assignment[employee] == space)
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()
