from z3 import *

# Variables
bay_cargo = Array('bay_cargo', IntSort(), IntSort())
Grain_bay = Int('Grain_bay')
Livestock_bay = Int('Livestock_bay')
Textiles_bay = Int('Textiles_bay')
Produce_bay = Int('Produce_bay')
Fuel_bay = Int('Fuel_bay')
Machinery_bay = Int('Machinery_bay')
b = Int('b')

solver = Solver()

# Constraints
solver.add(ForAll([b], Implies(And(b >= 1, b <= 6), And(bay_cargo[b] >= 0, bay_cargo[b] <= 5))))
solver.add(Distinct([bay_cargo[i] for i in range(1, 7)]))

solver.add(And(Grain_bay >= 1, Grain_bay <= 6))
solver.add(And(Livestock_bay >= 1, Livestock_bay <= 6))
solver.add(And(Textiles_bay >= 1, Textiles_bay <= 6))
solver.add(And(Produce_bay >= 1, Produce_bay <= 6))
solver.add(And(Fuel_bay >= 1, Fuel_bay <= 6))
solver.add(And(Machinery_bay >= 1, Machinery_bay <= 6))


solver.add(bay_cargo[Grain_bay] > bay_cargo[Livestock_bay])
solver.add(bay_cargo[Livestock_bay] > bay_cargo[Textiles_bay])
solver.add(bay_cargo[Produce_bay] > bay_cargo[Fuel_bay])
solver.add(Or(Produce_bay == Textiles_bay + 1, Textiles_bay == Produce_bay + 1))
solver.add(bay_cargo[4] == 4)  # Produce in bay 4


# Determine number of bays with determined cargo
determined_bays = 0
for bay in range(1, 7):
    possible_cargo_types = 0
    for cargo in range(0, 6):
        solver.push()
        solver.add(bay_cargo[bay] == cargo)
        if solver.check() == sat:
            possible_cargo_types += 1
        solver.pop()
    if possible_cargo_types == 1:
        determined_bays += 1

# Check against answer choices
if determined_bays == 2:
    print("Option A is correct")
elif determined_bays == 3:
    print("Option B is correct")
elif determined_bays == 4:
    print("Option C is correct")
elif determined_bays == 5:
    print("Option D is correct")
elif determined_bays == 6:
    print("Option E is correct")