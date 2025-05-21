from z3 import *

# Define variables
assignment = Array('assignment', IntSort(), IntSort())
solver = Solver()
c = Int('c')

# Constraints
solver.add(ForAll([c], And(assignment[c] >= 0, assignment[c] < 5)))
solver.add(Distinct([assignment[0], assignment[1], assignment[2]]))
solver.add(Xor(Or(assignment[0] == 1, assignment[1] == 1, assignment[2] == 1), Or(assignment[0] == 3, assignment[1] == 3, assignment[2] == 3)))
solver.add(Implies(Or(assignment[0] == 0, assignment[1] == 0, assignment[2] == 0), Or(assignment[0] == 1, assignment[1] == 1, assignment[2] == 1)))
solver.add(Implies(assignment[0] == 4, assignment[1] != 1))
solver.add(Implies(Or(assignment[0] == 2, assignment[1] == 2, assignment[2] == 2), assignment[2] == 2))

# Kayne assigned to Yemen
solver.add(assignment[1] == 1)

# Check answer choices
options = [
    assignment[0] == 0,  # A
    assignment[2] == 2,  # B
    assignment[2] == 4,  # C
    And(assignment[0] != 0, assignment[1] != 0, assignment[2] != 0),  # D
    And(assignment[0] != 4, assignment[1] != 4, assignment[2] != 4)   # E
]

for i, option in enumerate(options):
    solver.push()
    solver.add(Not(option))
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()