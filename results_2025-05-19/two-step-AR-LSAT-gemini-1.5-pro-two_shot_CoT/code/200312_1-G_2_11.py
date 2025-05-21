from z3 import *

# Define constants for cargo types
F = 0
G = 1
L = 2
M = 3
P = 4
T = 5

# Define the variable
bay_of_cargo = Array('bay_of_cargo', IntSort(), IntSort())

# Create the solver
solver = Solver()

# Constraint 1 (Domain)
c = Int('c')
solver.add(ForAll([c], Implies(And(c >= 0, c <= 5), And(bay_of_cargo[c] >= 1, bay_of_cargo[c] <= 6))))

# Constraint 2 (Distinctness)
solver.add(Distinct([bay_of_cargo[i] for i in range(6)]))

# Constraint 3 (Grain > Livestock)
solver.add(bay_of_cargo[G] > bay_of_cargo[L])

# Constraint 4 (Livestock > Textiles)
solver.add(bay_of_cargo[L] > bay_of_cargo[T])

# Constraint 5 (Produce > Fuel)
solver.add(bay_of_cargo[P] > bay_of_cargo[F])

# Constraint 6 (Textiles next to Produce)
solver.add(Or(bay_of_cargo[T] == bay_of_cargo[P] + 1, bay_of_cargo[T] == bay_of_cargo[P] - 1))

# Constraint 7 (Produce next to Livestock)
solver.add(Or(bay_of_cargo[P] == bay_of_cargo[L] + 1, bay_of_cargo[P] == bay_of_cargo[L] - 1))

# Check each answer choice
answer_choices = [
    (F, 2),  # Bay 2 is holding fuel.
    (P, 4),  # Bay 4 is holding produce.
    (T, 4),  # Bay 4 is holding textiles.
    (G, 5),  # Bay 5 is holding grain.
    (M, 5),  # Bay 5 is holding machinery.
]

for i, (cargo, bay) in enumerate(answer_choices):
    solver.push()
    solver.add(bay_of_cargo[cargo] == bay)
    if solver.check() == unsat:
        print(f'Option {chr(65 + i)} is correct')
        exit()
    solver.pop()