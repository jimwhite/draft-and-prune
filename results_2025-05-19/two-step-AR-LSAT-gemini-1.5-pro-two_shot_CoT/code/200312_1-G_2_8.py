from z3 import *

# Constants for cargo types
F = 0
G = 1
L = 2
M = 3
P = 4
T = 5

# Variables
bay_cargo = Array('bay_cargo', IntSort(), IntSort())

# Solver
solver = Solver()

# Constraint 0 (Domain)
i = Int('i')
solver.add(ForAll([i], Implies(And(i >= 1, i <= 6), And(bay_cargo[i] >= 0, bay_cargo[i] <= 5))))

# Constraint 1 (Distinctness)
solver.add(Distinct([bay_cargo[i] for i in range(1, 7)]))

# Constraint 2 (Grain > Livestock)
i = Int('i')
j = Int('j')
solver.add(ForAll([i, j], Implies(And(i >= 1, i <= 6, j >= 1, j <= 6, bay_cargo[i] == G, bay_cargo[j] == L), i > j)))

# Constraint 3 (Livestock > Textiles)
i = Int('i')
j = Int('j')
solver.add(ForAll([i, j], Implies(And(i >= 1, i <= 6, j >= 1, j <= 6, bay_cargo[i] == L, bay_cargo[j] == T), i > j)))

# Constraint 4 (Produce > Fuel)
i = Int('i')
j = Int('j')
solver.add(ForAll([i, j], Implies(And(i >= 1, i <= 6, j >= 1, j <= 6, bay_cargo[i] == P, bay_cargo[j] == F), i > j)))

# Constraint 5 (Textiles next to Produce)
i = Int('i')
solver.add(Or(Exists([i], And(i >= 1, i < 6, bay_cargo[i] == T, bay_cargo[i+1] == P)), Exists([i], And(i >= 1, i < 6, bay_cargo[i] == P, bay_cargo[i+1] == T))))

# Constraint 6 (Machinery and Grain separated by one bay)
i = Int('i')
solver.add(Or(Exists([i], And(i >= 1, i < 5, bay_cargo[i] == M, bay_cargo[i+2] == G)), Exists([i], And(i >= 1, i < 5, bay_cargo[i] == G, bay_cargo[i+2] == M))))


# Answering the Question
determined_bays = 0
for i in range(1, 7):
    possible_cargo_types = 0
    for c in range(6):
        solver.push()
        solver.add(bay_cargo[i] == c)
        if solver.check() == sat:
            possible_cargo_types += 1
        solver.pop()
    if possible_cargo_types == 1:
        determined_bays += 1

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