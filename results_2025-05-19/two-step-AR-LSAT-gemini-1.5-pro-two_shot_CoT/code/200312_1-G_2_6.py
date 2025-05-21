from z3 import *

# Define cargo types
F = 0
G = 1
L = 2
M = 3
P = 4
T = 5

# Define bay_cargo array
bay_cargo = Array('bay_cargo', IntSort(), IntSort())

# Create solver
solver = Solver()

# Constraint 0 (Domain)
i = Int('i')
solver.add(ForAll([i], Implies(And(i >= 1, i <= 6), And(bay_cargo[i] >= 0, bay_cargo[i] <= 5))))

# Constraint 1 (Distinctness)
solver.add(Distinct([bay_cargo[i] for i in range(1, 7)]))

# Constraint 2 (Grain > Livestock)
i = Int('i')
j = Int('j')
solver.add(ForAll([i, j], Implies(And(bay_cargo[i] == G, bay_cargo[j] == L, i >= 1, i <= 6, j >= 1, j <= 6), i > j)))

# Constraint 3 (Livestock > Textiles)
i = Int('i')
j = Int('j')
solver.add(ForAll([i, j], Implies(And(bay_cargo[i] == L, bay_cargo[j] == T, i >= 1, i <= 6, j >= 1, j <= 6), i > j)))

# Constraint 4 (Produce > Fuel)
i = Int('i')
j = Int('j')
solver.add(ForAll([i, j], Implies(And(bay_cargo[i] == P, bay_cargo[j] == F, i >= 1, i <= 6, j >= 1, j <= 6), i > j)))

# Constraint 5 (Textiles next to Produce)
i = Int('i')
solver.add(Or([And(bay_cargo[i] == T, bay_cargo[i+1] == P, i >= 1, i < 6), And(bay_cargo[i] == P, bay_cargo[i-1] == T, i > 1, i <= 6)]))

# Check answer choices
options = [
    And(bay_cargo[1] == F, bay_cargo[2] == M, bay_cargo[3] == T),
    And(bay_cargo[1] == G, bay_cargo[2] == M, bay_cargo[3] == F),
    And(bay_cargo[1] == M, bay_cargo[2] == L, bay_cargo[3] == F),
    And(bay_cargo[1] == M, bay_cargo[2] == T, bay_cargo[3] == F),
    And(bay_cargo[1] == M, bay_cargo[2] == T, bay_cargo[3] == P)
]

for i, option in enumerate(options):
    solver.push()
    solver.add(option)
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()