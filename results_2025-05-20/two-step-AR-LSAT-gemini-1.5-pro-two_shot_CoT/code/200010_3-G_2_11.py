from z3 import *

# Variables
selected_works = Array('selected_works', IntSort(), BoolSort())

# Solver
solver = Solver()

# Constraints
solver.add(Sum([If(selected_works[i], 1, 0) for i in range(9)]) >= 5)
solver.add(Sum([If(selected_works[i], 1, 0) for i in range(9)]) <= 6)
solver.add(Sum([If(selected_works[i], 1, 0) for i in [0, 1, 2, 6, 7]]) <= 4)
solver.add(Sum([If(selected_works[i], 1, 0) for i in range(6)]) >= 3)
solver.add(Sum([If(selected_works[i], 1, 0) for i in range(6)]) <= 4)
solver.add(Sum([If(selected_works[i], 1, 0) for i in range(3)]) >= Sum([If(selected_works[i], 1, 0) for i in range(3, 6)]))
solver.add(Implies(And(selected_works[6], selected_works[7]), Not(selected_works[8])))

# Answer choices
options = [
    And(Sum([If(selected_works[i], 1, 0) for i in range(3, 6)]) == 0, Sum([If(selected_works[i], 1, 0) for i in range(6, 9)]) == 1),
    And(Sum([If(selected_works[i], 1, 0) for i in range(3, 6)]) == 1, selected_works[6], selected_works[7]),
    And(Sum([If(selected_works[i], 1, 0) for i in range(3)]) == 2, selected_works[8]),
    And(Sum([If(selected_works[i], 1, 0) for i in range(3)]) == 2, Sum([If(selected_works[i], 1, 0) for i in range(6, 9)]) == 2),
    And(Sum([If(selected_works[i], 1, 0) for i in range(3, 6)]) == 2, Sum([If(selected_works[i], 1, 0) for i in range(6, 9)]) == 1)
]

# Check each option
for i, option in enumerate(options):
    solver.push()
    solver.add(option)
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()
