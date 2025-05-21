from z3 import *

# Define variables
composition_at_slot = Array('composition_at_slot', IntSort(), IntSort())
i = Int('i')
j = Int('j')

# Define solver and add constraints
solver = Solver()

# Constraint 0 (Domain)
solver.add(ForAll([i], And(composition_at_slot[i] >= 0, composition_at_slot[i] <= 7)))

# Constraint 1 (Distinctness)
solver.add(Distinct([composition_at_slot[i] for i in range(8)]))

# Constraint 2 (T before F or after R)
solver.add(Or(Exists([i], And(i >= 0, i < 7, composition_at_slot[i] == 7, composition_at_slot[i+1] == 0)),
               Exists([i], And(i >= 1, i < 8, composition_at_slot[i] == 7, composition_at_slot[i-1] == 5))))

# Constraint 3 (Two between F and R)
solver.add(Or(Exists([i, j], And(i >= 0, i < 8, j >= 0, j < 8, composition_at_slot[i] == 0, composition_at_slot[j] == 5, j - i > 2)),
               Exists([i, j], And(i >= 0, i < 8, j >= 0, j < 8, composition_at_slot[i] == 0, composition_at_slot[j] == 5, i - j > 2))))

# Constraint 4 (O first or fifth)
solver.add(Or(composition_at_slot[0] == 3, composition_at_slot[4] == 3))

# Constraint 5 (L or H eighth)
solver.add(Or(composition_at_slot[7] == 2, composition_at_slot[7] == 1))

# Constraint 6 (P before S)
solver.add(Exists([i, j], And(i >= 0, i < 8, j >= 0, j < 8, i < j, composition_at_slot[i] == 4, composition_at_slot[j] == 6)))

# Constraint 7 (One between O and S)
solver.add(Or(Exists([i, j], And(i >= 0, i < 8, j >= 0, j < 8, composition_at_slot[i] == 3, composition_at_slot[j] == 6, j - i > 1)),
               Exists([i, j], And(i >= 0, i < 8, j >= 0, j < 8, composition_at_slot[i] == 3, composition_at_slot[j] == 6, i - j > 1))))

# Answer choices
options = [
    [2, 4, 6, 5, 3, 7, 0, 1],
    [3, 7, 4, 0, 6, 1, 5, 2],
    [4, 7, 0, 6, 2, 5, 3, 1],
    [4, 7, 0, 6, 3, 5, 2, 1],
    [7, 0, 4, 5, 3, 2, 6, 1]
]

# Check each option
for option_index, option in enumerate(options):
    solver.push()
    for slot, composition in enumerate(option):
        solver.add(composition_at_slot[slot] == composition)
    if solver.check() == sat:
        print(f"Option {chr(65 + option_index)} is correct")
        exit()
    solver.pop()