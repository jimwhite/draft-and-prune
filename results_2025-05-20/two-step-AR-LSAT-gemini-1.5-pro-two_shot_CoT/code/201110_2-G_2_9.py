from z3 import *

# Define variables
assignment = Array('assignment', IntSort(), IntSort())
solver = Solver()

# Constraints
solver.add(Distinct([assignment[0], assignment[1], assignment[2]]))
solver.add(Xor(Or(assignment[0] == 1, assignment[1] == 1, assignment[2] == 1), Or(assignment[0] == 3, assignment[1] == 3, assignment[2] == 3)))
solver.add(Implies(Or(assignment[0] == 0, assignment[1] == 0, assignment[2] == 0), Or(assignment[0] == 1, assignment[1] == 1, assignment[2] == 1)))
solver.add(Implies(assignment[0] == 4, assignment[1] != 1))
solver.add(Implies(Or(assignment[0] == 2, assignment[1] == 2, assignment[2] == 2), assignment[2] == 2))

# Premise: Ong assigned to Venezuela
solver.add(assignment[0] == 4)

# Answer choices
choices = [
    Or(And(assignment[1] == 0, assignment[2] == 2), And(assignment[2] == 0, assignment[1] == 2)),  # Jaramillo and Landon
    Or(And(assignment[1] == 0, assignment[2] == 3), And(assignment[2] == 0, assignment[1] == 3)),  # Jaramillo and Novetzke
    Or(And(assignment[1] == 1, assignment[2] == 2), And(assignment[2] == 1, assignment[1] == 2)),  # Kayne and Landon
    Or(And(assignment[1] == 1, assignment[2] == 3), And(assignment[2] == 1, assignment[1] == 3)),  # Kayne and Novetzke
    Or(And(assignment[1] == 2, assignment[2] == 3), And(assignment[2] == 2, assignment[1] == 3))   # Landon and Novetzke
]

for i, choice in enumerate(choices):
    solver.push()
    solver.add(choice)
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()