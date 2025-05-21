from z3 import *

# Define variables
assignment = Array('assignment', IntSort(), IntSort())

# Create solver and add general constraints
solver = Solver()

# Constraint 1 (Domain)
solver.add(And(assignment[0] >= 0, assignment[0] < 5, assignment[1] >= 0, assignment[1] < 5, assignment[2] >= 0, assignment[2] < 5))

# Constraint 2 (Distinctness)
solver.add(Distinct([assignment[0], assignment[1], assignment[2]]))

# Constraint 3 (Kayne/Novetzke XOR)
solver.add(Xor(Or(assignment[0] == 1, assignment[1] == 1, assignment[2] == 1), Or(assignment[0] == 3, assignment[1] == 3, assignment[2] == 3)))

# Constraint 4 (Jaramillo implies Kayne)
solver.add(Implies(Or(assignment[0] == 0, assignment[1] == 0, assignment[2] == 0), Or(assignment[0] == 1, assignment[1] == 1, assignment[2] == 1)))

# Constraint 5 (Ong to Venezuela implies Kayne not to Yemen)
solver.add(Implies(assignment[0] == 4, assignment[1] != 1))

# Constraint 6 (Landon to Zambia)
solver.add(Implies(Or(assignment[0] == 2, assignment[1] == 2, assignment[2] == 2), assignment[2] == 2))

# Answer choices
options = [
    [0, 4, 3],  # Venezuela: Jaramillo, Yemen: Ong, Zambia: Novetzke
    [1, 0, 2],  # Venezuela: Kayne, Yemen: Jaramillo, Zambia: Landon
    [2, 3, 4],  # Venezuela: Landon, Yemen: Novetzke, Zambia: Ong
    [3, 0, 1],  # Venezuela: Novetzke, Yemen: Jaramillo, Zambia: Kayne
    [4, 1, 2]   # Venezuela: Ong, Yemen: Kayne, Zambia: Landon
]

# Check each option
for i, option in enumerate(options):
    solver.push()
    solver.add(assignment[0] == option[0])
    solver.add(assignment[1] == option[1])
    solver.add(assignment[2] == option[2])
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()