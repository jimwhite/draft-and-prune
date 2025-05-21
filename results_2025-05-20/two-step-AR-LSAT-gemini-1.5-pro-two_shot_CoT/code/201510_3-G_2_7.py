from z3 import *

# Define variables
counts = [[Int('count_%s_%s' % (p, s)) for s in range(3)] for p in range(3)]

# Create solver and add constraints
solver = Solver()

# Constraint 1: Domain of counts
for p in range(3):
    for s in range(3):
        solver.add(counts[p][s] >= 0, counts[p][s] <= 2)

# Constraint 2: Two photos per section
for s in range(3):
    solver.add(Sum([counts[p][s] for p in range(3)]) == 2)

# Constraint 3: At least one photo per photographer
for p in range(3):
    solver.add(Sum([counts[p][s] for s in range(3)]) >= 1)

# Constraint 4: At most three photos per photographer
for p in range(3):
    solver.add(Sum([counts[p][s] for s in range(3)]) <= 3)

# Constraint 5: Lifestyle/Metro overlap
solver.add(Or([And(counts[p][0] >= 1, counts[p][1] >= 1) for p in range(3)]))

# Constraint 6: Hue in Lifestyle and Fuentes in Sports
solver.add(counts[2][0] == counts[0][2])

# Constraint 7: No Gagnon in Sports
solver.add(counts[1][2] == 0)

# Check answer choices
choices = [
    [[2, 0, 0], [1, 0, 1], [0, 1, 1]],  # A
    [[1, 1, 0], [1, 1, 0], [0, 0, 2]],  # B
    [[2, 0, 0], [0, 2, 0], [0, 0, 2]],  # C
    [[0, 2, 0], [1, 1, 0], [1, 0, 1]],  # D
    [[0, 1, 1], [0, 0, 2], [1, 0, 1]]   # E
]

for i, choice in enumerate(choices):
    solver.push()
    for p in range(3):
        for s in range(3):
            solver.add(counts[p][s] == choice[p][s])
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()
