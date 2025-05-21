from z3 import *

# Variables
on_team = Array('on_team', IntSort(), BoolSort())

# Solver
solver = Solver()

# Constraints
solver.add(Sum([If(on_team[i], 1, 0) for i in range(8)]) >= 4)
solver.add(Implies(on_team[0], And(Not(on_team[1]), Not(on_team[2]))))
solver.add(Implies(on_team[3], And(on_team[2], on_team[4])))
solver.add(Implies(on_team[5], And(on_team[0], on_team[6])))

# Answer choices
pairs = [[0, 4], [1, 6], [2, 7], [3, 5], [5, 6]]
options = ["A", "B", "C", "D", "E"]

for i, pair in enumerate(pairs):
    solver.push()
    solver.add(And(on_team[pair[0]], on_team[pair[1]]))
    if solver.check() == unsat:
        print(f"Option {options[i]} is correct")
        exit()
    solver.pop()