from z3 import *

# Variables
assignment = Array('assignment', IntSort(), IntSort())

# Solver
solver = Solver()

c = Int('c')

# Constraints
solver.add(ForAll([c], And(assignment[c] >= 0, assignment[c] < 5)))
solver.add(Distinct([assignment[0], assignment[1], assignment[2]]))
solver.add(Xor(Exists([c], assignment[c] == 1), Exists([c], assignment[c] == 3)))
solver.add(Implies(Exists([c], assignment[c] == 0), Exists([c], assignment[c] == 1)))
solver.add(Implies(assignment[0] == 4, assignment[1] != 1))
solver.add(Implies(Exists([c], assignment[c] == 2), assignment[2] == 2))

# Ong assigned to Venezuela
solver.add(assignment[0] == 4)

# Answer choices
options = [
    ["Jaramillo and Landon", And(Or(And(assignment[1] == 0, assignment[2] == 2), And(assignment[1] == 2, assignment[2] == 0)), assignment[0] != 0, assignment[0] != 2)],
    ["Jaramillo and Novetzke", And(Or(And(assignment[1] == 0, assignment[2] == 3), And(assignment[1] == 3, assignment[2] == 0)), assignment[0] != 0, assignment[0] != 3)],
    ["Kayne and Landon", And(Or(And(assignment[1] == 1, assignment[2] == 2), And(assignment[1] == 2, assignment[2] == 1)), assignment[0] != 1, assignment[0] != 2)],
    ["Kayne and Novetzke", And(Or(And(assignment[1] == 1, assignment[2] == 3), And(assignment[1] == 3, assignment[2] == 1)), assignment[0] != 1, assignment[0] != 3)],
    ["Landon and Novetzke", And(Or(And(assignment[1] == 2, assignment[2] == 3), And(assignment[1] == 3, assignment[2] == 2)), assignment[0] != 2, assignment[0] != 3)]
]

# Check options
for i, (option_text, option_constraint) in enumerate(options):
    solver.push()
    solver.add(option_constraint)
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()