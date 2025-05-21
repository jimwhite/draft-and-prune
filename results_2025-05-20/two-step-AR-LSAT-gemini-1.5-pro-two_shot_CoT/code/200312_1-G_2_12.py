from z3 import *

# Variables
bay_of_Fuel = Int('bay_of_Fuel')
bay_of_Grain = Int('bay_of_Grain')
bay_of_Livestock = Int('bay_of_Livestock')
bay_of_Machinery = Int('bay_of_Machinery')
bay_of_Produce = Int('bay_of_Produce')
bay_of_Textiles = Int('bay_of_Textiles')

# Solver
solver = Solver()

# Constraints
solver.add(And(bay_of_Fuel >= 1, bay_of_Fuel <= 6,
               bay_of_Grain >= 1, bay_of_Grain <= 6,
               bay_of_Livestock >= 1, bay_of_Livestock <= 6,
               bay_of_Machinery >= 1, bay_of_Machinery <= 6,
               bay_of_Produce >= 1, bay_of_Produce <= 6,
               bay_of_Textiles >= 1, bay_of_Textiles <= 6))
solver.add(Distinct([bay_of_Fuel, bay_of_Grain, bay_of_Livestock, bay_of_Machinery, bay_of_Produce, bay_of_Textiles]))
solver.add(bay_of_Grain > bay_of_Livestock)
solver.add(bay_of_Livestock > bay_of_Textiles)
solver.add(bay_of_Produce > bay_of_Fuel)
solver.add(Abs(bay_of_Textiles - bay_of_Produce) == 1)
solver.add(bay_of_Produce == 4)

# Answering the question
determined_bays_count = 0
cargo_vars = [bay_of_Fuel, bay_of_Grain, bay_of_Livestock, bay_of_Machinery, bay_of_Produce, bay_of_Textiles]
cargo_names = ["Fuel", "Grain", "Livestock", "Machinery", "Produce", "Textiles"]

for b in range(1, 7):
    possible_cargo_types_at_b = []
    for i, cargo_var in enumerate(cargo_vars):
        solver.push()
        solver.add(cargo_var == b)
        if solver.check() == sat:
            possible_cargo_types_at_b.append(cargo_names[i])
        solver.pop()
    if len(possible_cargo_types_at_b) == 1:
        determined_bays_count += 1

answer_choices = ["two", "three", "four", "five", "six"]
if determined_bays_count == 4:
    print("Option C is correct")
    exit()