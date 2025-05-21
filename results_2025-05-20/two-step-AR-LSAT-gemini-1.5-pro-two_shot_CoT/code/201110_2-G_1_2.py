from z3 import *

R, S, T, V, X, Y = 0, 1, 2, 3, 4, 5

assignment = Array('assignment', IntSort(), IntSort())
solver = Solver()

# Constraint 1: Distinct Assignments
solver.add(Distinct([assignment[i] for i in range(6)]))

# Constraint 2: Parking Space Range
solver.add(And([And(assignment[i] >= 0, assignment[i] <= 5) for i in range(6)]))

# Constraint 3: Young > Togowa
solver.add(assignment[Y] > assignment[T])

# Constraint 4: Xu > Souza
solver.add(assignment[X] > assignment[S])

# Constraint 5: Robertson > Young
solver.add(assignment[R] > assignment[Y])

# Constraint 6: Robertson's Parking Space
solver.add(Or(assignment[R] == 0, assignment[R] == 1, assignment[R] == 2, assignment[R] == 3))

# Constraint 7: Togowa > Souza
solver.add(assignment[T] > assignment[S])

options = [
    (Y, 1),  # A: Young is assigned #2
    (V, 4),  # B: Vaughn is assigned #5
    (T, 2),  # C: Togowa is assigned #3
    (S, 1),  # D: Souza is assigned #2
    (R, 2)   # E: Robertson is assigned #3
]

for i, (employee, space) in enumerate(options):
    solver.push()
    solver.add(assignment[employee] == space)
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()