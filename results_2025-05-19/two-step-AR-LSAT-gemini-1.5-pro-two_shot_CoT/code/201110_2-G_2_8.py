from z3 import *

# Variables
assignment = Array('assignment', IntSort(), IntSort())
c = Int('c')

# Solver
solver = Solver()

# Constraints
solver.add(ForAll([c], And(assignment[c] >= 0, assignment[c] < 5)))  # Domain
solver.add(Distinct([assignment[0], assignment[1], assignment[2]]))  # Distinctness
solver.add(Xor(Or(assignment[0] == 1, assignment[1] == 1, assignment[2] == 1), Or(assignment[0] == 3, assignment[1] == 3, assignment[2] == 3)))  # Kayne XOR Novetzke
solver.add(Implies(Or(assignment[0] == 0, assignment[1] == 0, assignment[2] == 0), Or(assignment[0] == 1, assignment[1] == 1, assignment[2] == 1)))  # Jaramillo implies Kayne
solver.add(Implies(assignment[0] == 4, assignment[1] != 1))  # Ong to Venezuela implies Kayne not to Yemen
solver.add(Implies(Or(assignment[0] == 2, assignment[1] == 2, assignment[2] == 2), assignment[2] == 2))  # Landon to Zambia

# Answer choices
options = [
    [0, 3],  # Jaramillo and Novetzke
    [0, 4],  # Jaramillo and Ong
    [1, 2],  # Kayne and Landon
    [1, 3],  # Kayne and Novetzke
    [2, 4]   # Landon and Ong
]

for i, option in enumerate(options):
    solver.push()
    solver.add(Not(Or(assignment[0] == option[0], assignment[1] == option[0], assignment[2] == option[0])))
    solver.add(Not(Or(assignment[0] == option[1], assignment[1] == option[1], assignment[2] == option[1])))
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()