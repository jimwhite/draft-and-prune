from z3 import *

# Variables
on_team = Array('on_team', IntSort(), BoolSort())

# Solver
solver = Solver()

# Constraints
solver.add(Sum([If(on_team[i], 1, 0) for i in range(8)]) >= 4)
solver.add(Implies(on_team[0], Not(Or(on_team[1], on_team[2]))))
solver.add(Implies(on_team[3], And(on_team[2], on_team[4])))
solver.add(Implies(on_team[5], And(on_team[0], on_team[6])))

# Answer choices
choices = [(1, 3), (1, 5), (2, 3), (4, 6), (6, 7)]
choice_letters = ['A', 'B', 'C', 'D', 'E']

# Check each answer choice
for i, (emp1, emp2) in enumerate(choices):
    solver.push()
    solver.add(Not(Or(on_team[emp1], on_team[emp2])))
    if solver.check() == unsat:
        print(f"Option {choice_letters[i]} is correct")
        exit()
    solver.pop()