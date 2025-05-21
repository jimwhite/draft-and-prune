from z3 import *

# Variables
assignment = [[Int(f"assignment_{d}_{r}") for r in range(4)] for d in range(2)]

# Solver
solver = Solver()

# General Constraints
for d in range(2):
    solver.add(Distinct(assignment[d]))
    for r in range(4):
        solver.add(And(assignment[d][r] >= 0, assignment[d][r] <= 3))

for d in range(2):
    solver.add(assignment[d][0] != 0)  # Reynaldo cannot test F
    solver.add(assignment[d][3] != 3)  # Yuki cannot test J

solver.add(Or(assignment[0][2] == 2, assignment[1][2] == 2))  # Theresa must test H

solver.add(assignment[1][1] == assignment[0][3])  # Yuki's Day 1 bike is Seamus's Day 2 bike

for r in range(4):
    solver.add(assignment[0][r] != assignment[1][r])  # Different bikes per rider per day


# Question Premise
solver.add(assignment[0][2] == 3)  # Theresa tests J on Day 1

# Answer Choices
options = [
    assignment[1][0] == 1,  # A: Reynaldo tests G on Day 2
    assignment[0][1] == 2,  # B: Seamus tests H on Day 1
    assignment[1][3] == 2,  # C: Yuki tests H on Day 2
    Or(assignment[0][1] == 3, assignment[1][1] == 3),  # D: Seamus is one of the testers for J
    Or(assignment[0][2] == 1, assignment[1][2] == 1)  # E: Theresa is one of the testers for G
]

for i, option in enumerate(options):
    solver.push()
    solver.add(option)
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()
