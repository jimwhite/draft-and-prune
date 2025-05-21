from z3 import *

# Define variables
solo_order = Array('solo_order', IntSort(), IntSort())

# Create solver
solver = Solver()

# Constraint 1: Distinctness
solver.add(Distinct([solo_order[i] for i in range(6)]))

# Constraint 2: Guitarist not 4th
solver.add(solo_order[3] != 0)

# Constraint 3: Percussionist before Keyboard player
solver.add(Sum([If(solo_order[i] == 2, 1, 0) for i in range(6)]) < Sum([If(solo_order[i] == 1, 1, 0) for i in range(6)]))

# Constraint 4: Violinist before Keyboard player before Guitarist
solver.add(Sum([If(solo_order[i] == 5, 1, 0) for i in range(6)]) < Sum([If(solo_order[i] == 1, 1, 0) for i in range(6)]))
solver.add(Sum([If(solo_order[i] == 1, 1, 0) for i in range(6)]) < Sum([If(solo_order[i] == 0, 1, 0) for i in range(6)]))

# Constraint 5: Saxophonist after Percussionist or Trumpeter, but not both
solver.add(Xor(Sum([If(solo_order[i] == 2, 1, 0) for i in range(6)]) < Sum([If(solo_order[i] == 3, 1, 0) for i in range(6)]), Sum([If(solo_order[i] == 4, 1, 0) for i in range(6)]) < Sum([If(solo_order[i] == 3, 1, 0) for i in range(6)])))

# Answer choices
choices = [
    [5, 2, 3, 0, 4, 1],  # A
    [2, 5, 1, 4, 3, 0],  # B
    [5, 4, 3, 2, 1, 0],  # C
    [1, 4, 5, 3, 0, 2],  # D
    [0, 5, 1, 2, 3, 4]   # E
]

# Check each choice
for i, choice in enumerate(choices):
    solver.push()
    for j in range(6):
        solver.add(solo_order[j] == choice[j])
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()

