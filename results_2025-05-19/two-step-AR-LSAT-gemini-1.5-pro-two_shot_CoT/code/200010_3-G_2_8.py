from z3 import *

# Variables
selected_works = Array('selected_works', IntSort(), BoolSort())

# Solver
solver = Solver()

# Constraints
solver.add(Sum([If(selected_works[i], 1, 0) for i in range(9)]) >= 5)
solver.add(Sum([If(selected_works[i], 1, 0) for i in range(9)]) <= 6)
solver.add(Sum([If(selected_works[i], 1, 0) for i in range(5)]) <= 4)
solver.add(Sum([If(selected_works[i], 1, 0) for i in range(6)]) >= 3)
solver.add(Sum([If(selected_works[i], 1, 0) for i in range(6)]) <= 4)
solver.add(Sum([If(selected_works[i], 1, 0) for i in range(3)]) >= Sum([If(selected_works[i], 1, 0) for i in range(3, 6)]))
solver.add(Implies(And(selected_works[6], selected_works[7]), Not(selected_works[8])))

# Answer choices
choices = [
    And(Not(selected_works[3]), Not(selected_works[4]), Not(selected_works[5])),
    Sum([If(selected_works[i], 1, 0) for i in range(3)]) == 1,
    And(selected_works[6], selected_works[7], selected_works[8]),
    And(selected_works[3], selected_works[4], selected_works[5]),
    And(selected_works[0], selected_works[1], selected_works[2], selected_works[6], selected_works[7])
]

for i in range(len(choices)):
    solver.push()
    solver.add(choices[i])
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()
