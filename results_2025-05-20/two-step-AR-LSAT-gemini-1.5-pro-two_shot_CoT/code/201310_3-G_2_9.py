from z3 import *

# Define boolean variables for each employee
on_team = [Bool(f"on_team_{i}") for i in range(8)]

# Define the solver
solver = Solver()

# Constraint: At least four employees on the team
solver.add(Sum([If(on_team[i], 1, 0) for i in range(8)]) >= 4)

# Constraint: If Myers is on the team, neither Ortega nor Paine can be
solver.add(Implies(on_team[0], And(Not(on_team[1]), Not(on_team[2]))))

# Constraint: If Schmidt is on the team, both Paine and Thomson must also be
solver.add(Implies(on_team[3], And(on_team[2], on_team[4])))

# Constraint: If Wong is on the team, both Myers and Yoder must also be
solver.add(Implies(on_team[5], And(on_team[0], on_team[6])))

# Answer choices:
pairs = [(0, 4), (1, 6), (2, 7), (3, 5), (5, 6)]  # Employee indices for each pair
options = ["A", "B", "C", "D", "E"]

# Check each answer choice
for i, (p1, p2) in enumerate(pairs):
    solver.push()
    solver.add(And(on_team[p1], on_team[p2]))
    if solver.check() == unsat:
        print(f"Option {options[i]} is correct")
        exit()
    solver.pop()