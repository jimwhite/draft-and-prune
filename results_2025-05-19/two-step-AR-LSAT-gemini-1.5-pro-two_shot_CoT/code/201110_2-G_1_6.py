from z3 import *

# Define constants for employees and parking spaces
R, S, T, V, X, Y = 0, 1, 2, 3, 4, 5

# Define the parking assignment variable (array)
parking_assignment = Array('parking_assignment', IntSort(), IntSort())

# Create a Z3 solver instance
solver = Solver()

# Constraint 1: Domain (0 <= parking_assignment[i] <= 5)
i = Int('i')
solver.add(ForAll([i], Implies(And(i >= 0, i < 6), And(parking_assignment[i] >= 0, parking_assignment[i] <= 5))))

# Constraint 2: Distinctness
solver.add(Distinct([parking_assignment[i] for i in range(6)]))

# Constraint 3: Young > Togowa
solver.add(parking_assignment[Y] > parking_assignment[T])

# Constraint 4: Xu > Souza
solver.add(parking_assignment[X] > parking_assignment[S])

# Constraint 5: Robertson > Young
solver.add(parking_assignment[R] > parking_assignment[Y])

# Constraint 6: Robertson's options
solver.add(Or(parking_assignment[R] == 0, parking_assignment[R] == 1, parking_assignment[R] == 2, parking_assignment[R] == 3))

# Add constraint: Robertson is assigned parking space #3
solver.add(parking_assignment[R] == 2)

# Answer choices and their negations
answer_choices = [
    (S, 3),  # A: Souza is assigned parking space #4
    (T, 1),  # B: Togowa is assigned parking space #2
    (V, 4),  # C: Vaughn is assigned parking space #5
    (X, 5),  # D: Xu is assigned parking space #6
    (Y, 1)   # E: Young is assigned parking space #2
]

for option, (employee, space) in enumerate(answer_choices):
    solver.push()
    solver.add(Not(parking_assignment[employee] == space))
    if solver.check() == unsat:
        print(f"Option {chr(65 + option)} is correct")
        exit()
    solver.pop()