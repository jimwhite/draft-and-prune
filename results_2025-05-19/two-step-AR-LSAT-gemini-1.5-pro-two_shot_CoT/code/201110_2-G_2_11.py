from z3 import *

# Variables
assignment = Array('assignment', IntSort(), IntSort())

# Solver
solver = Solver()

# Constraints
c = Int('c')
solver.add(ForAll([c], And(assignment[c] >= 0, assignment[c] < 5)))  # Domain
solver.add(Distinct([assignment[0], assignment[1], assignment[2]]))  # Distinctness
solver.add(Xor(Or(assignment[0] == 1, assignment[1] == 1, assignment[2] == 1), Or(assignment[0] == 3, assignment[1] == 3, assignment[2] == 3)))  # Kayne XOR Novetzke
solver.add(Implies(Or(assignment[0] == 0, assignment[1] == 0, assignment[2] == 0), Or(assignment[0] == 1, assignment[1] == 1, assignment[2] == 1)))  # Jaramillo implies Kayne
solver.add(Implies(assignment[0] == 4, assignment[1] != 1))  # Ong to Venezuela implies not Kayne to Yemen
solver.add(Implies(Or(assignment[0] == 2, assignment[1] == 2, assignment[2] == 2), assignment[2] == 2))  # Landon implies Zambia

# Answer choices
options = [
    Not(assignment[2] == 0),  # A
    Not(assignment[2] == 1),  # B
    Not(assignment[2] == 3),  # C
    And(assignment[0] != 2, assignment[1] != 2, assignment[2] != 2),  # D
    And(assignment[0] != 4, assignment[1] != 4, assignment[2] != 4)   # E
]

# Check each option
for i, option in enumerate(options):
    solver.push()
    solver.add(option)
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()