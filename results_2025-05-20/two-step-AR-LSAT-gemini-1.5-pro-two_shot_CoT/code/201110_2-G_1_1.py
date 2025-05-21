from z3 import *

# Define employee IDs and parking space indices
R, S, T, V, X, Y = 0, 1, 2, 3, 4, 5
spaces = [0, 1, 2, 3, 4, 5]

# Define the variable: space[employee_id] = space_index
space = Array('space', IntSort(), IntSort())

# Create the solver
solver = Solver()

# Constraint 0 (Domain)
i = Int('i')
solver.add(ForAll([i], Implies(And(i >= 0, i <= 5), And(space[i] >= 0, space[i] <= 5))))

# Constraint 1 (Distinctness)
solver.add(Distinct([space[i] for i in range(6)]))

# Constraint 2 (Young > Togowa)
solver.add(space[Y] > space[T])

# Constraint 3 (Xu > Souza)
solver.add(space[X] > space[S])

# Constraint 4 (Robertson > Young)
solver.add(space[R] > space[Y])

# Constraint 5 (Robertson's Parking Space)
solver.add(Or(space[R] == 0, space[R] == 1, space[R] == 2, space[R] == 3))

# Answer choices
options = [
    [(Y, 0), (S, 1), (V, 2), (R, 3), (T, 4), (X, 5)],
    [(V, 0), (T, 1), (Y, 2), (S, 3), (R, 4), (X, 5)],
    [(T, 0), (Y, 1), (X, 2), (R, 3), (S, 4), (V, 5)],
    [(T, 0), (R, 1), (Y, 2), (S, 3), (V, 4), (X, 5)],
    [(S, 0), (T, 1), (Y, 2), (R, 3), (X, 4), (V, 5)]
]

# Check each option
for option_index, option in enumerate(options):
    solver.push()
    for employee, parking_space in option:
        solver.add(space[employee] == parking_space)
    if solver.check() == sat:
        print(f"Option {chr(65 + option_index)} is correct")
        exit()
    solver.pop()