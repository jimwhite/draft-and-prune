from z3 import *

# Constants for employees and parking spaces
R, S, T, V, X, Y = 0, 1, 2, 3, 4, 5

# Variable: assignment[i] is the parking space of employee i
assignment = Array('assignment', IntSort(), IntSort())

solver = Solver()

# Constraint 1: Domain
i = Int('i')
solver.add(ForAll([i], Implies(And(i >= 0, i <= 5), And(assignment[i] >= 0, assignment[i] <= 5))))

# Constraint 2: Distinctness
solver.add(Distinct([assignment[i] for i in range(6)]))

# Constraint 3: Young > Togowa
solver.add(assignment[Y] > assignment[T])

# Constraint 4: Xu > Souza
solver.add(assignment[X] > assignment[S])

# Constraint 5: Robertson > Young
solver.add(assignment[R] > assignment[Y])

# Constraint 6: Robertson's Parking Space
solver.add(Or(assignment[R] == 0, assignment[R] == 1, assignment[R] == 2, assignment[R] == 3))

# Answer choices
choices = [
    (S, 0),  # Souza is assigned parking space #1
    (Y, 1),  # Young is assigned parking space #2
    (V, 2),  # Vaughn is assigned parking space #3
    (R, 3),  # Robertson is assigned parking space #4
    (X, 4)   # Xu is assigned parking space #5
]

for option, (employee, space) in enumerate(choices):
    solver.push()
    solver.add(assignment[employee] == space)
    if solver.check() == sat:
        model = solver.model()
        # Corrected: Use model.eval() to get the value of assignment[i]
        current_assignments = [assignment[i] == model.eval(assignment[i]) for i in range(6)]
        solver.push()
        solver.add(Not(And(current_assignments)))
        if solver.check() == unsat:
            print(f"Option {chr(65 + option)} is correct")
            exit()
        solver.pop()
    solver.pop()
