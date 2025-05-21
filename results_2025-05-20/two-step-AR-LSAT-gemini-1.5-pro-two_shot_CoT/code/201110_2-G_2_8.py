from z3 import *

# Define variables
assignment = Array('assignment', IntSort(), IntSort())

# Create solver and add base constraints
solver = Solver()

# Constraint 1 (Domain and Distinctness)
solver.add(Distinct(assignment[0], assignment[1], assignment[2]))
solver.add(And(assignment[0] >= 0, assignment[0] <= 4, assignment[1] >= 0, assignment[1] <= 4, assignment[2] >= 0, assignment[2] <= 4))

# Constraint 2 (Kayne XOR Novetzke)
solver.add(Xor(Or(assignment[0] == 1, assignment[1] == 1, assignment[2] == 1), Or(assignment[0] == 3, assignment[1] == 3, assignment[2] == 3)))

# Constraint 3 (Jaramillo implies Kayne)
solver.add(Implies(Or(assignment[0] == 0, assignment[1] == 0, assignment[2] == 0), Or(assignment[0] == 1, assignment[1] == 1, assignment[2] == 1)))

# Constraint 4 (Ong in Venezuela implies Kayne not in Yemen)
solver.add(Implies(assignment[0] == 4, assignment[1] != 1))

# Constraint 5 (Landon implies Zambia)
solver.add(Implies(Or(assignment[0] == 2, assignment[1] == 2, assignment[2] == 2), assignment[2] == 2))

# Answer choices
answer_choices = [
    (0, 3),  # Jaramillo and Novetzke
    (0, 4),  # Jaramillo and Ong
    (1, 2),  # Kayne and Landon
    (1, 3),  # Kayne and Novetzke
    (2, 4)   # Landon and Ong
]

# Check each answer choice
for i, (id1, id2) in enumerate(answer_choices):
    solver.push()
    solver.add(Not(Or(assignment[0] == id1, assignment[1] == id1, assignment[2] == id1)))
    solver.add(Not(Or(assignment[0] == id2, assignment[1] == id2, assignment[2] == id2)))
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()