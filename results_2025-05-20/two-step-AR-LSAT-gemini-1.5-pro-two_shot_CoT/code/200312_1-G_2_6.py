from z3 import *

# Variables
bay_cargo = Array('bay_cargo', IntSort(), IntSort())

# Cargo type mapping: F=0, G=1, L=2, M=3, P=4, T=5
cargo_map = {'f': 0, 'g': 1, 'l': 2, 'm': 3, 'p': 4, 't': 5}

solver = Solver()

# Constraint 1 (Domain)
i = Int('i') # Define i before using it
solver.add(ForAll([i], Implies(And(i >= 1, i <= 6), And(bay_cargo[i] >= 0, bay_cargo[i] <= 5))))

# Constraint 2 (Distinctness)
solver.add(Distinct([bay_cargo[i] for i in range(1, 7)]))

# Constraint 3 (Grain > Livestock)
i = Int('i')
j = Int('j')
solver.add(Exists([i, j], And(bay_cargo[i] == 1, bay_cargo[j] == 2, i > j, i >= 1, i <= 6, j >= 1, j <= 6)))

# Constraint 4 (Livestock > Textiles)
i = Int('i')
j = Int('j')
solver.add(Exists([i, j], And(bay_cargo[i] == 2, bay_cargo[j] == 5, i > j, i >= 1, i <= 6, j >= 1, j <= 6)))

# Constraint 5 (Produce > Fuel)
i = Int('i')
j = Int('j')
solver.add(Exists([i, j], And(bay_cargo[i] == 4, bay_cargo[j] == 0, i > j, i >= 1, i <= 6, j >= 1, j <= 6)))

# Constraint 6 (Textiles next to Produce)
i = Int('i')
solver.add(Exists([i], And(i >= 1, i <= 5, Or(And(bay_cargo[i] == 5, bay_cargo[i+1] == 4), And(bay_cargo[i] == 4, bay_cargo[i+1] == 5)))))

# Answer choices
options = [
    "fuel, machinery, textiles",
    "grain, machinery, fuel",
    "machinery, livestock, fuel",
    "machinery, textiles, fuel",
    "machinery, textiles, produce"
]

for option_index, option in enumerate(options):
    solver.push()
    cargo_types = [cargo_map[cargo.strip().lower()] for cargo in option.split(',')]
    for bay, cargo_type in enumerate(cargo_types, start=1): # Fixed: Start enumerate from 1
        solver.add(bay_cargo[bay] == cargo_type)
    if solver.check() == sat:
        print(f"Option {chr(65 + option_index)} is correct")
        exit()
    solver.pop()

