from z3 import *

# Variables
on_panel = Array('on_panel', IntSort(), BoolSort())

# Solver
solver = Solver()

# Constraints
solver.add(Sum([If(on_panel[i], 1, 0) for i in range(9)]) == 5)  # Constraint 1
solver.add(Or(on_panel[0], on_panel[1], on_panel[2]))  # Constraint 2 (Botanists)
solver.add(Or(on_panel[3], on_panel[4], on_panel[5]))  # Constraint 2 (Chemists)
solver.add(Or(on_panel[6], on_panel[7], on_panel[8]))  # Constraint 2 (Zoologists)
solver.add(Implies(Sum([If(on_panel[i], 1, 0) for i in range(3)]) > 1, Sum([If(on_panel[i], 1, 0) for i in range(6, 9)]) <= 1))  # Constraint 3
solver.add(Not(And(on_panel[0], on_panel[3])))  # Constraint 4
solver.add(Not(And(on_panel[3], on_panel[5])))  # Constraint 5
solver.add(Implies(on_panel[5], And(on_panel[6], on_panel[8])))  # Constraint 6
solver.add(And(on_panel[5], Not(on_panel[3]), Not(on_panel[4])))  # Constraint 7

# Answer choices
choices = [
    Not(And(on_panel[0], on_panel[1])),  # A
    Not(And(on_panel[1], on_panel[2])),  # B
    Not(And(on_panel[2], on_panel[6])),  # C
    Not(And(on_panel[0], on_panel[1], on_panel[2])),  # D
    Not(And(on_panel[6], on_panel[7], on_panel[8]))   # E
]

for i in range(len(choices)):
    solver.push()
    solver.add(choices[i])
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()