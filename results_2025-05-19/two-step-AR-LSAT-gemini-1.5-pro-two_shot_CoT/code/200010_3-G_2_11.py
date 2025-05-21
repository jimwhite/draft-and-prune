from z3 import *

# Variables
selected_works = Array('selected_works', IntSort(), BoolSort())

# Solver
solver = Solver()

# Constraints
solver.add(Sum([If(selected_works[i], 1, 0) for i in range(9)]) >= 5)
solver.add(Sum([If(selected_works[i], 1, 0) for i in range(9)]) <= 6)
solver.add(Sum([If(selected_works[i], 1, 0) for i in range(0,3)] + [If(selected_works[i], 1, 0) for i in range(6,8)]) <= 4)
solver.add(Sum([If(selected_works[i], 1, 0) for i in range(0,3)] + [If(selected_works[i], 1, 0) for i in range(3,6)]) >= 3)
solver.add(Sum([If(selected_works[i], 1, 0) for i in range(0,3)] + [If(selected_works[i], 1, 0) for i in range(3,6)]) <= 4)
solver.add(Sum([If(selected_works[i], 1, 0) for i in range(0,3)]) >= Sum([If(selected_works[i], 1, 0) for i in range(3, 6)]))
solver.add(Implies(And(selected_works[6], selected_works[7]), Not(selected_works[8])))

# Answer choices
choices = [
    Or(Sum([If(selected_works[i], 1, 0) for i in range(3, 6)]) != 0, Sum([If(selected_works[i], 1, 0) for i in range(6, 9)]) != 1),
    Or(Sum([If(selected_works[i], 1, 0) for i in range(3, 6)]) != 1, Not(And(selected_works[6], selected_works[7]))),
    Or(Sum([If(selected_works[i], 1, 0) for i in range(0,3)]) != 2, Not(selected_works[8])),
    Or(Sum([If(selected_works[i], 1, 0) for i in range(0,3)]) != 2, Sum([If(selected_works[i], 1, 0) for i in range(6, 9)]) != 2),
    Or(Sum([If(selected_works[i], 1, 0) for i in range(3, 6)]) != 2, Sum([If(selected_works[i], 1, 0) for i in range(6, 9)]) != 1)
]

for i, choice in enumerate(choices):
    solver.push()
    solver.add(choice)
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()
