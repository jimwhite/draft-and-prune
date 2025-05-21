from z3 import *

# Variables
assignment = Array('assignment', IntSort(), IntSort())

# Constraints
Constraint_0 = And(assignment[0] >= 0, assignment[0] < 5, assignment[1] >= 0, assignment[1] < 5, assignment[2] >= 0, assignment[2] < 5)
Constraint_1 = Distinct([assignment[0], assignment[1], assignment[2]])
Constraint_2 = Xor(Or(assignment[0] == 1, assignment[1] == 1, assignment[2] == 1), Or(assignment[0] == 3, assignment[1] == 3, assignment[2] == 3))
Constraint_3 = Implies(Or(assignment[0] == 0, assignment[1] == 0, assignment[2] == 0), Or(assignment[0] == 1, assignment[1] == 1, assignment[2] == 1))
Constraint_4 = Implies(assignment[0] == 4, assignment[1] != 1)
Constraint_5 = Implies(Or(assignment[0] == 2, assignment[1] == 2, assignment[2] == 2), assignment[2] == 2)

# Base Constraints
Base = And(Constraint_0, Constraint_1, Constraint_2, Constraint_4, Constraint_5)

# Alternative Constraints
C_A = Implies(Or(assignment[0] == 1, assignment[1] == 1, assignment[2] == 1), Or(assignment[0] == 0, assignment[1] == 0, assignment[2] == 0))
C_B = Implies(And(Or(assignment[0] == 4, assignment[1] == 4, assignment[2] == 4), Or(assignment[0] == 2, assignment[1] == 2, assignment[2] == 2)), Or(assignment[0] == 3, assignment[1] == 3, assignment[2] == 3))
C_C = Implies(Not(Or(assignment[0] == 4, assignment[1] == 4, assignment[2] == 4)), Or(assignment[0] == 1, assignment[1] == 1, assignment[2] == 1))
C_D = Not(And(Or(assignment[0] == 0, assignment[1] == 0, assignment[2] == 0), Or(assignment[0] == 3, assignment[1] == 3, assignment[2] == 3)))
C_E = Not(And(Or(assignment[0] == 3, assignment[1] == 3, assignment[2] == 3), Or(assignment[0] == 4, assignment[1] == 4, assignment[2] == 4)))

# Solver
solver = Solver()
solver.add(Base)

# Check Answer Choices
choices = [C_A, C_B, C_C, C_D, C_E]
for i, choice in enumerate(choices):
    solver.push()
    solver.add(And(Constraint_3, Not(choice)))
    result1 = solver.check()
    solver.pop()

    solver.push()
    solver.add(And(choice, Not(Constraint_3)))
    result2 = solver.check()
    solver.pop()

    if result1 == unsat and result2 == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()