from z3 import *

# Variables
assignment = Array('assignment', IntSort(), IntSort())

# Solver
solver = Solver()

# Constraints
solver.add(And(assignment[0] >= 0, assignment[0] < 5, assignment[1] >= 0, assignment[1] < 5, assignment[2] >= 0, assignment[2] < 5))
solver.add(Distinct([assignment[0], assignment[1], assignment[2]]))
solver.add(Xor(Or(assignment[0] == 1, assignment[1] == 1, assignment[2] == 1), Or(assignment[0] == 3, assignment[1] == 3, assignment[2] == 3)))
solver.add(Implies(Or(assignment[0] == 0, assignment[1] == 0, assignment[2] == 0), Or(assignment[0] == 1, assignment[1] == 1, assignment[2] == 1)))
solver.add(Implies(assignment[0] == 4, assignment[1] != 1))
solver.add(Implies(Or(assignment[0] == 2, assignment[1] == 2, assignment[2] == 2), assignment[2] == 2))
solver.add(assignment[1] == 1)

# Answer choices
answer_choices = [
    Not(assignment[0] == 0),
    Not(assignment[2] == 2),
    Not(assignment[2] == 4),
    Or(assignment[0] == 0, assignment[1] == 0, assignment[2] == 0),
    Or(assignment[0] == 4, assignment[1] == 4, assignment[2] == 4)
]

# Check each answer choice
for i in range(len(answer_choices)):
    solver.push()
    solver.add(answer_choices[i])
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()