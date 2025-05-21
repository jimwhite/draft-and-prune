from z3 import *

# Variables
on_panel = Array('on_panel', IntSort(), BoolSort())

# Solver
solver = Solver()

# Constraints
# Constraint 1: Panel Size
solver.add(Sum([If(on_panel[i], 1, 0) for i in range(9)]) == 5)

# Constraint 2: At least one of each type
solver.add(Or(on_panel[0], on_panel[1], on_panel[2]))  # Botanist
solver.add(Or(on_panel[3], on_panel[4], on_panel[5]))  # Chemist
solver.add(Or(on_panel[6], on_panel[7], on_panel[8]))  # Zoologist

# Constraint 3: More than one botanist implies at most one zoologist
solver.add(Implies(Sum([If(on_panel[i], 1, 0) for i in range(3)]) > 1,
                   Sum([If(on_panel[i], 1, 0) for i in range(6, 9)]) <= 1))

# Constraint 4: F and K mutual exclusion
solver.add(Not(And(on_panel[0], on_panel[3])))

# Constraint 5: K and M mutual exclusion
solver.add(Not(And(on_panel[3], on_panel[5])))

# Constraint 6: M implies P and R
solver.add(Implies(on_panel[5], And(on_panel[6], on_panel[8])))

# Constraint 7: M is the only chemist
solver.add(And(on_panel[5], Not(on_panel[3]), Not(on_panel[4])))

# Check answer choices
answer_choices = [
    And(on_panel[0], on_panel[1]),  # F and G
    And(on_panel[1], on_panel[2]),  # G and H
    And(on_panel[2], on_panel[6]),  # H and P
    And(on_panel[0], on_panel[1], on_panel[2]),  # F, G, and H
    And(on_panel[6], on_panel[7], on_panel[8])   # P, Q, and R
]

for i, choice in enumerate(answer_choices):
    solver.push()
    solver.add(Not(choice))
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()