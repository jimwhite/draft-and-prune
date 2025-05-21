from z3 import *

# Variables
on_team = Array('on_team', IntSort(), BoolSort())

# Solver
solver = Solver()

# Constraints
solver.add(Sum([If(on_team[i], 1, 0) for i in range(8)]) >= 4)
solver.add(Implies(on_team[0], Not(on_team[1])))
solver.add(Implies(on_team[0], Not(on_team[2])))
solver.add(Implies(on_team[3], And(on_team[2], on_team[4])))
solver.add(Implies(on_team[5], And(on_team[0], on_team[6])))

# Answer choices
choices = [
    [0, 2, 3, 4],
    [1, 2, 4, 7],
    [2, 3, 6, 7],
    [3, 4, 6, 7],
    [4, 5, 6, 7]
]

# Check each choice
for i, choice in enumerate(choices):
    solver.push()
    for j in range(8):
        if j in choice:
            solver.add(on_team[j] == True)
        else:
            solver.add(on_team[j] == False)
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()