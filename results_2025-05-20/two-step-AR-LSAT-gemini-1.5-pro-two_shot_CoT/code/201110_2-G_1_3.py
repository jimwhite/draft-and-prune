from z3 import *

# Employee indices
R_index = 0
S_index = 1
T_index = 2
V_index = 3
X_index = 4
Y_index = 5

# Create Z3 array for assignments
assignment = Array('assignment', IntSort(), IntSort())

# Create solver and add constraints
solver = Solver()

# Constraint 1: Domain (Corrected: Use list comprehension instead of generator)
solver.add([And(assignment[i] >= 0, assignment[i] < 6) for i in range(6)])

# Constraint 2: Distinctness
solver.add(Distinct([assignment[i] for i in range(6)]))

# Constraint 3: Young > Togowa
solver.add(assignment[Y_index] > assignment[T_index])

# Constraint 4: Xu > Souza
solver.add(assignment[X_index] > assignment[S_index])

# Constraint 5: Robertson > Young
solver.add(assignment[R_index] > assignment[Y_index])

# Constraint 6: Robertson's options
solver.add(assignment[R_index] <= 3)

# Check answer choices
answer_choices = [
    (S_index, 0),  # Souza assigned #1
    (Y_index, 1),  # Young assigned #2
    (V_index, 2),  # Vaughn assigned #3
    (R_index, 3),  # Robertson assigned #4
    (X_index, 4)   # Xu assigned #5
]

for choice_index, (employee_index, space_index) in enumerate(answer_choices):
    solver.push()
    solver.add(assignment[employee_index] == space_index)
    if solver.check() == sat:
        model = solver.model()
        solver.push()
        # Corrected: Access model values correctly
        model_equalities = [assignment[i] == model.eval(assignment[i]) for i in range(6)]
        solver.add(Not(And(model_equalities)))
        if solver.check() == unsat:
            print(f"Option {chr(65 + choice_index)} is correct")
            exit()
        solver.pop()
    solver.pop()
