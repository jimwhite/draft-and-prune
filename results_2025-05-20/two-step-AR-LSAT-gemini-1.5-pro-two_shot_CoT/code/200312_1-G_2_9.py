from z3 import *

# Define cargo type IDs
F = 0
G = 1
L = 2
M = 3
P = 4
T = 5

# Define bay_cargo array
bay_cargo = Array('bay_cargo', IntSort(), IntSort())

# Define Abs function
Abs = lambda x: If(x >= 0, x, -x)

# Create solver and add constraints
solver = Solver()

# Constraint 0: Domain
solver.add(ForAll([i], Implies(And(i >= 1, i <= 6), And(bay_cargo[i] >= 0, bay_cargo[i] <= 5))))

# Constraint 1: Distinctness
solver.add(Distinct([bay_cargo[i] for i in range(1, 7)]))

# Constraint 2: Grain > Livestock
solver.add(ForAll([i, j], Implies(And(bay_cargo[i] == G, bay_cargo[j] == L, i >=1, i <= 6, j >= 1, j <= 6), i > j)))

# Constraint 3: Livestock > Textiles
solver.add(ForAll([i, j], Implies(And(bay_cargo[i] == L, bay_cargo[j] == T, i >=1, i <= 6, j >= 1, j <= 6), i > j)))

# Constraint 4: Produce > Fuel
solver.add(ForAll([i, j], Implies(And(bay_cargo[i] == P, bay_cargo[j] == F, i >=1, i <= 6, j >= 1, j <= 6), i > j)))

# Constraint 5: Textiles next to Produce
solver.add(ForAll([i, j], Implies(And(bay_cargo[i] == T, bay_cargo[j] == P, i >=1, i <= 6, j >= 1, j <= 6), Abs(i - j) == 1)))


# Check answer choices
bays = [1, 2, 3, 5, 6]
option_letter = 'A'

for bay in bays:
    solver.push()
    solver.add(bay_cargo[bay] == L)
    if solver.check() == sat:
        print(f"Option {option_letter} is correct")
        exit()
    solver.pop()
    option_letter = chr(ord(option_letter) + 1)
