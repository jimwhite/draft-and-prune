from z3 import *

# Define variables
counts = [[Int('c_%s_%s' % (p, s)) for s in range(3)] for p in range(3)]

# Create solver
solver = Solver()

# Constraint 1: Photographer photo counts
for p in range(3):
    solver.add(Sum(counts[p]) >= 1)
    solver.add(Sum(counts[p]) <= 3)

# Constraint 2: Two photos per section
for s in range(3):
    solver.add(Sum([counts[p][s] for p in range(3)]) == 2) # Corrected Sum to use a list comprehension

# Constraint 3: Lifestyle/Metro overlap
solver.add(Or(counts[0][0] > 0, counts[1][0] > 0, counts[2][0] > 0))

# Constraint 4: Hue in Lifestyle and Fuentes in Sports
solver.add(counts[2][0] == counts[0][2])

# Constraint 5: No Gagnon in Sports
solver.add(counts[1][2] == 0)


# Check answer choices
options = [
    [[2, 0, 0], [1, 0, 1], [0, 1, 1]],  # A
    [[1, 1, 0], [1, 1, 0], [0, 0, 2]],  # B
    [[2, 0, 0], [0, 2, 0], [0, 0, 2]],  # C
    [[0, 2, 0], [1, 1, 0], [1, 0, 1]],  # D
    [[0, 1, 1], [0, 0, 2], [1, 1, 0]]   # E
]

for i, option in enumerate(options):
    solver.push()
    for p in range(3):
        for s in range(3):
            solver.add(counts[p][s] == option[p][s])
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()
