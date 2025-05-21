from z3 import *

# Variables
assignment = Array('assignment', IntSort(), IntSort())

# Solver
solver = Solver()

# Constraints
c = Int('c')
solver.add(ForAll([c], And(assignment[c] >= 0, assignment[c] < 5))) # Constraint 1: Domain
solver.add(Distinct([assignment[0], assignment[1], assignment[2]])) # Constraint 2: Distinctness
solver.add(Or(And(Or(assignment[0] == 1, assignment[1] == 1, assignment[2] == 1), Not(Or(assignment[0] == 3, assignment[1] == 3, assignment[2] == 3))), And(Not(Or(assignment[0] == 1, assignment[1] == 1, assignment[2] == 1)), Or(assignment[0] == 3, assignment[1] == 3, assignment[2] == 3)))) # Constraint 3: Kayne XOR Novetzke
solver.add(Implies(Or(assignment[0] == 0, assignment[1] == 0, assignment[2] == 0), Or(assignment[0] == 1, assignment[1] == 1, assignment[2] == 1))) # Constraint 4: Jaramillo implies Kayne
solver.add(Implies(assignment[0] == 4, assignment[1] != 1)) # Constraint 5: Ong to Venezuela implies not Kayne to Yemen
solver.add(Implies(Or(assignment[0] == 2, assignment[1] == 2), False)) # Constraint 6: Landon implies Zambia


# Answer choices
options = [
    [[0, 0], [1, 4], [2, 3]],  # A
    [[0, 1], [1, 0], [2, 2]],  # B
    [[0, 2], [1, 3], [2, 4]],  # C
    [[0, 3], [1, 0], [2, 1]],  # D
    [[0, 4], [1, 1], [2, 2]]   # E
]

# Check each option
for i, option in enumerate(options):
    solver.push()
    for country, ambassador in option:
        solver.add(assignment[country] == ambassador)
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()