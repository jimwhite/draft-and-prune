from z3 import *

# Variables
assignment = Array('assignment', IntSort(), IntSort())

# Solver
solver = Solver()

# Constraints 1-5
for day in range(2):
    for rider in range(4):
        solver.add(0 <= assignment[day, rider], assignment[day, rider] < 4)
    solver.add(Distinct([assignment[day, rider] for rider in range(4)]))

for rider in range(4):
    solver.add(assignment[0, rider] != assignment[1, rider])

# Constraints 6-9
for day in range(2):
    solver.add(assignment[day, 0] != 0)  # Reynaldo cannot test F
    solver.add(assignment[day, 3] != 3)  # Yuki cannot test J

solver.add(Or(assignment[0, 2] == 2, assignment[1, 2] == 2))  # Theresa must test H
solver.add(assignment[0, 3] == assignment[1, 1])  # Yuki's day 1 bicycle is Seamus's day 2 bicycle

# Answer choices
choices = [
    Or(And(assignment[0, 0] == 3, assignment[0, 1] == 3), And(assignment[1, 0] == 3, assignment[1, 1] == 3)),  # A
    Or(And(assignment[0, 0] == 3, assignment[0, 2] == 3), And(assignment[1, 0] == 3, assignment[1, 2] == 3)),  # B
    Or(And(assignment[0, 0] == 1, assignment[0, 3] == 1), And(assignment[1, 0] == 1, assignment[1, 3] == 1)),  # C
    Or(And(assignment[0, 1] == 1, assignment[0, 2] == 1), And(assignment[1, 1] == 1, assignment[1, 2] == 1)),  # D
    Or(And(assignment[0, 2] == 0, assignment[0, 3] == 0), And(assignment[1, 2] == 0, assignment[1, 3] == 0))   # E
]

for i, choice in enumerate(choices):
    solver.push()
    solver.add(choice)
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()
