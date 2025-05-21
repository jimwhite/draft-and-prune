from z3 import *

# Variables
on_team = Array('on_team', IntSort(), BoolSort())

# Solver
solver = Solver()

# Constraints
solver.add(Sum([If(on_team[i], 1, 0) for i in range(8)]) >= 4)  # Constraint 1
solver.add(Implies(on_team[0], And(Not(on_team[1]), Not(on_team[2]))))  # Constraint 2
solver.add(Implies(on_team[3], And(on_team[2], on_team[4])))  # Constraint 3
solver.add(Implies(on_team[5], And(on_team[0], on_team[6])))  # Constraint 4
solver.add(Not(on_team[2]))  # Constraint 5

# Answer choices
choices = [
    And(Not(on_team[0]), Not(on_team[1])),  # A
    And(Not(on_team[0]), Not(on_team[4])),  # B
    And(Not(on_team[0]), Not(on_team[7])),  # C
    And(Not(on_team[1]), Not(on_team[4])),  # D
    And(Not(on_team[1]), Not(on_team[6]))   # E
]

# Check each choice
for i in range(len(choices)):
    solver.push()
    solver.add(choices[i])
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()