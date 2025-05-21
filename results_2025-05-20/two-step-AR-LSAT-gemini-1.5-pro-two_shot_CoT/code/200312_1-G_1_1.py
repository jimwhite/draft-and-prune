from z3 import *

# Define variables
on_panel = Array('on_panel', IntSort(), BoolSort())

# Create solver and add base constraints
solver = Solver()

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

# Answer choices
choices = [
    [0, 1, 3, 6, 7],
    [1, 2, 3, 4, 5],
    [1, 2, 3, 4, 8],
    [2, 3, 5, 6, 8],
    [2, 4, 5, 6, 7]
]

# Check each answer choice
for i, choice in enumerate(choices):
    solver.push()
    for j in range(9):
        solver.add(on_panel[j] == (j in choice))
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()