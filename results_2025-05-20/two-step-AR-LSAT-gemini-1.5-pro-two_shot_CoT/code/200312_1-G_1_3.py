from z3 import *

# Variables
on_panel = Array('on_panel', IntSort(), BoolSort())

# Solver
solver = Solver()

# Constraints
# Constraint 0: Panel Size
solver.add(Sum([If(on_panel[i], 1, 0) for i in range(9)]) == 5)

# Constraint 1: At least one of each type
solver.add(Or(on_panel[0], on_panel[1], on_panel[2]))  # Botanist
solver.add(Or(on_panel[3], on_panel[4], on_panel[5]))  # Chemist
solver.add(Or(on_panel[6], on_panel[7], on_panel[8]))  # Zoologist

# Constraint 2: More than one botanist implies at most one zoologist
solver.add(Implies(Sum([If(on_panel[i], 1, 0) for i in range(3)]) > 1,
                   Sum([If(on_panel[i], 1, 0) for i in range(6, 9)]) <= 1))

# Constraint 3: F and K cannot both be selected
solver.add(Not(And(on_panel[0], on_panel[3])))

# Constraint 4: K and M cannot both be selected
solver.add(Not(And(on_panel[3], on_panel[5])))

# Constraint 5: If M is selected, both P and R must be selected
solver.add(Implies(on_panel[5], And(on_panel[6], on_panel[8])))

# Given: F, L, Q, and R are on the panel
solver.add(on_panel[0] == True)
solver.add(on_panel[4] == True)
solver.add(on_panel[7] == True)
solver.add(on_panel[8] == True)

# Check answer choices
choices = [1, 2, 3, 5, 6]  # G, H, K, M, P
option_letter = 'A'
for choice in choices:
    solver.push()
    solver.add(on_panel[choice] == False)
    if solver.check() == unsat:
        print(f"Option {option_letter} is correct")
        exit()
    solver.pop()
    option_letter = chr(ord(option_letter) + 1)