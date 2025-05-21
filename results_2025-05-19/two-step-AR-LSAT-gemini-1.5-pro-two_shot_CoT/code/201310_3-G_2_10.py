from z3 import *

# Variables
on_team = Array('on_team', IntSort(), BoolSort())

# Solver
solver = Solver()

# Constraints
# Constraint 1 (Team Size)
solver.add(Sum([If(on_team[i], 1, 0) for i in range(8)]) >= 4)

# Constraint 2 (Myers/Ortega/Paine)
solver.add(Implies(on_team[0], Not(Or(on_team[1], on_team[2]))))

# Constraint 3 (Schmidt/Paine/Thomson)
solver.add(Implies(on_team[3], And(on_team[2], on_team[4])))

# Constraint 4 (Wong/Myers/Yoder)
solver.add(Implies(on_team[5], And(on_team[0], on_team[6])))

# Constraint 5 (Yoder not on team)
solver.add(Not(on_team[6]))

# Answer Choices
employees = ["Myers", "Ortega", "Paine", "Thomson", "Zayre"]
employee_indices = [0, 1, 2, 4, 7]

for i, index in enumerate(employee_indices):
    solver.push()
    solver.add(on_team[index])
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()