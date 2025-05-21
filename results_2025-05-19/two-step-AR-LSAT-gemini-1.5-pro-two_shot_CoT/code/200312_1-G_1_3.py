from z3 import *

# Define variables
selected = [Bool(f'selected_{i}') for i in range(9)]

# Create solver and add constraints
solver = Solver()

# Constraint 1: Panel Size
solver.add(Sum([If(selected[i], 1, 0) for i in range(9)]) == 5)

# Constraint 2: At least one of each type
solver.add(Or(selected[0], selected[1], selected[2]))  # Botanist
solver.add(Or(selected[3], selected[4], selected[5]))  # Chemist
solver.add(Or(selected[6], selected[7], selected[8]))  # Zoologist

# Constraint 3: More than one botanist implies at most one zoologist
solver.add(Implies(Sum([If(selected[i], 1, 0) for i in range(3)]) > 1,
                   Sum([If(selected[i], 1, 0) for i in range(6, 9)]) <= 1))

# Constraint 4: F and K cannot both be selected
solver.add(Not(And(selected[0], selected[3])))

# Constraint 5: K and M cannot both be selected
solver.add(Not(And(selected[3], selected[5])))

# Constraint 6: If M is selected, both P and R must be selected
solver.add(Implies(selected[5], And(selected[6], selected[8])))

# Constraint 7: F, L, Q, and R are selected
solver.add(And(selected[0], selected[4], selected[7], selected[8]))

# Check answer choices
answers = [1, 2, 3, 5, 6]  # Indices of G, H, K, M, P
for i, idx in enumerate(answers):
    solver.push()
    solver.add(selected[idx])
    if solver.check() == sat:
        solver.pop()
        solver.push()
        solver.add(Not(selected[idx]))
        if solver.check() == unsat:
            print(f'Option {chr(65 + i)} is correct')
            exit()
        solver.pop()
    else:
        solver.pop()