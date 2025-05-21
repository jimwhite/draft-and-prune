from z3 import *

# Define variables
on_team = Array('on_team', IntSort(), BoolSort())

# Create solver and add constraints
solver = Solver()
solver.add(Sum([If(on_team[i], 1, 0) for i in range(8)]) >= 4)
solver.add(Implies(on_team[0], Not(Or(on_team[1], on_team[2]))))
solver.add(Implies(on_team[3], And(on_team[2], on_team[4])))
solver.add(Implies(on_team[5], And(on_team[0], on_team[6])))

# Answer choices
choices = [
    [1, 3],  # Ortega, Schmidt
    [1, 5],  # Ortega, Wong
    [2, 3],  # Paine, Schmidt
    [4, 6],  # Thomson, Yoder
    [6, 7]   # Yoder, Zayre
]

# Check each answer choice
for i, (e1, e2) in enumerate(choices):
    solver.push()
    solver.add(Not(Or(on_team[e1], on_team[e2])))
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()