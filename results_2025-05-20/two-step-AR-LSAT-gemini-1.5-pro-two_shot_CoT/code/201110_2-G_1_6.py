from z3 import *

# Entities (as integer IDs)
R, S, T, V, X, Y = 0, 1, 2, 3, 4, 5

# Variables
parking_assignment = Array('parking_assignment', IntSort(), IntSort())

# Solver
solver = Solver()

# Constraints
for i in range(6):
    solver.add(And(parking_assignment[i] >= 0, parking_assignment[i] <= 5))
solver.add(Distinct([parking_assignment[i] for i in range(6)]))
solver.add(parking_assignment[Y] > parking_assignment[T])
solver.add(parking_assignment[X] > parking_assignment[S])
solver.add(parking_assignment[R] > parking_assignment[Y])
solver.add(Or(parking_assignment[R] == 0, parking_assignment[R] == 1, parking_assignment[R] == 2, parking_assignment[R] == 3))
solver.add(parking_assignment[R] == 2)


# Check answer choices
answer_choices = [
    (S, 3),  # A
    (T, 1),  # B
    (V, 4),  # C
    (X, 5),  # D
    (Y, 1)   # E
]

for i, (employee, space) in enumerate(answer_choices):
    solver.push()
    solver.add(Not(parking_assignment[employee] == space))
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()