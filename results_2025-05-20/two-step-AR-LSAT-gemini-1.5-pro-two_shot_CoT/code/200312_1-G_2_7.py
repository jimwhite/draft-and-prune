from z3 import *

# Define cargo types
F = 0
G = 1
L = 2
M = 3
P = 4
T = 5

# Define variables
bay_cargo = Array('bay_cargo', IntSort(), IntSort())
i = Int('i')
j = Int('j')

# Create solver and add constraints
solver = Solver()

# Constraint 0 (Domain)
solver.add(ForAll([i], Implies(And(i >= 1, i <= 6), And(bay_cargo[i] >= 0, bay_cargo[i] <= 5))))

# Constraint 1 (Distinctness)
solver.add(Distinct([bay_cargo[k] for k in range(1, 7)]))

# Constraint 2 (Grain > Livestock)
solver.add(Exists([i, j], And(i >= 1, i <= 6, j >= 1, j <= 6, bay_cargo[i] == G, bay_cargo[j] == L, i > j)))

# Constraint 3 (Livestock > Textiles)
solver.add(Exists([i, j], And(i >= 1, i <= 6, j >= 1, j <= 6, bay_cargo[i] == L, bay_cargo[j] == T, i > j)))

# Constraint 4 (Produce > Fuel)
solver.add(Exists([i, j], And(i >= 1, i <= 6, j >= 1, j <= 6, bay_cargo[i] == P, bay_cargo[j] == F, i > j)))

# Constraint 5 (Textiles next to Produce)
solver.add(ForAll([i], Implies(And(i >= 1, i <= 6, bay_cargo[i] == T), Or(And(i > 1, bay_cargo[i-1] == P), And(i < 6, bay_cargo[i+1] == P)))))

# Check answer choices
answer_choices = ["grain", "livestock", "machinery", "produce", "textiles"]
cargo_ids = [G, L, M, P, T]

for choice_index, cargo_id in enumerate(cargo_ids):
    solver.push()
    solver.add(bay_cargo[4] == cargo_id)
    if solver.check() == unsat:
        print(f"Option {chr(65 + choice_index)} is correct")
        exit()
    solver.pop()