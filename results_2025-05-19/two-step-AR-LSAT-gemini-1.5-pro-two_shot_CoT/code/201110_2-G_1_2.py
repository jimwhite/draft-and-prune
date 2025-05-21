from z3 import *

R, S, T, V, X, Y = 0, 1, 2, 3, 4, 5  # Employee IDs

assignment = Array('assignment', IntSort(), IntSort())
solver = Solver()

# Constraint 1: Distinct Assignments
solver.add(Distinct([assignment[i] for i in [R, S, T, V, X, Y]]))

# Constraint 2: Parking Space Range
for i in [R, S, T, V, X, Y]:
    solver.add(And(assignment[i] >= 0, assignment[i] <= 5))

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
    assignment[Y] == 1,  # A
    assignment[V] == 4,  # B
    assignment[T] == 2,  # C
    assignment[S] == 1,  # D
    assignment[R] == 2   # E
]

for i, option in enumerate(options):
    solver.push()
    solver.add(option)
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()