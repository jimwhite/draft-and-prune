from z3 import *

# Variables
on_panel = Array('on_panel', IntSort(), BoolSort())

# Solver
solver = Solver()

# Constraints
solver.add(Sum([If(on_panel[i], 1, 0) for i in range(9)]) == 5)  # Constraint 1
solver.add(Or([on_panel[i] for i in range(3)]))  # Constraint 2 (Botanist)
solver.add(Or([on_panel[i] for i in range(3, 6)]))  # Constraint 2 (Chemist)
solver.add(Or([on_panel[i] for i in range(6, 9)]))  # Constraint 2 (Zoologist)
solver.add(Implies(Sum([If(on_panel[i], 1, 0) for i in range(3)]) > 1, Sum([If(on_panel[i], 1, 0) for i in range(6, 9)]) <= 1))  # Constraint 3
solver.add(Not(And(on_panel[0], on_panel[3])))  # Constraint 4
solver.add(Not(And(on_panel[3], on_panel[5])))  # Constraint 5
solver.add(Implies(on_panel[5], And(on_panel[6], on_panel[8])))  # Constraint 6
solver.add(And(on_panel[1], on_panel[2]))  # Constraint 7

# Answer choices
choices = [
    Not(Or(on_panel[0], on_panel[3])),  # A
    Not(Or(on_panel[0], on_panel[5])),  # B
    Not(Or(on_panel[3], on_panel[5])),  # C
    Not(Or(on_panel[5], on_panel[7])),  # D
    Not(Or(on_panel[6], on_panel[7]))   # E
]

for i, choice in enumerate(choices):
    solver.push()
    solver.add(choice)
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()