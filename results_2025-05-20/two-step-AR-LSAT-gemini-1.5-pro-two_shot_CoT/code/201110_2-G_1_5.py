from z3 import *

# Define variables
assignment = Array('assignment', IntSort(), IntSort())
employee_indices = [0, 1, 2, 3, 4, 5]
solver = Solver()

# Add constraints
solver.add(And([And(assignment[i] >= 0, assignment[i] < 6) for i in employee_indices]))  # Domain
solver.add(Distinct([assignment[i] for i in employee_indices]))  # Distinctness
solver.add(assignment[5] > assignment[2])  # Young > Togowa
solver.add(assignment[4] > assignment[1])  # Xu > Souza
solver.add(assignment[0] > assignment[5])  # Robertson > Young
solver.add(Or(assignment[0] == 0, assignment[0] == 1, assignment[0] == 2, assignment[0] == 3))  # Robertson's space
solver.add(assignment[5] > assignment[1])  # Young > Souza (Question condition)

# Check answer choices
choices = [(2, 0), (5, 1), (0, 2), (1, 2), (3, 3)]  # (employee_index, parking_space)
for i, (employee, space) in enumerate(choices):
    solver.push()
    solver.add(assignment[employee] == space)
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()