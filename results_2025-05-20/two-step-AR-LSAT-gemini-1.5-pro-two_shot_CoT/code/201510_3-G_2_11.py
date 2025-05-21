from z3 import *

# Variables
section_counts = [[Int('section_%s_%s' % (s, p)) for p in range(3)] for s in range(3)]

# Solver
solver = Solver()

# Constraints
# Constraint 1 (Two photos per section)
for s in range(3):
    solver.add(Sum(section_counts[s]) == 2)

# Constraint 2 (Photographer photo counts)
for p in range(3):
    solver.add(And(Sum([section_counts[s][p] for s in range(3)]) >= 1, Sum([section_counts[s][p] for s in range(3)]) <= 3))

# Constraint 3 (Lifestyle/Metro overlap)
solver.add(Or(And(section_counts[0][0] > 0, section_counts[1][0] > 0),
               And(section_counts[0][1] > 0, section_counts[1][1] > 0),
               And(section_counts[0][2] > 0, section_counts[1][2] > 0)))

# Constraint 4 (Hue/Fuentes balance)
solver.add(section_counts[0][2] == section_counts[2][0])

# Constraint 5 (No Gagnon in Sports)
solver.add(section_counts[2][1] == 0)

# Constraint 6 (Given condition - Lifestyle)
solver.add(section_counts[0][0] == 1)
solver.add(section_counts[0][2] == 1)
solver.add(section_counts[0][1] == 0)

# Non-negative counts
for s in range(3):
    for p in range(3):
        solver.add(section_counts[s][p] >= 0)


# Check answer choices
choices = [
    (section_counts[1][0] == 2),  # A
    (section_counts[1][1] == 2),  # B
    (section_counts[1][2] == 1),  # C
    (section_counts[2][2] == 2),  # D
    (section_counts[2][2] == 0)   # E
]

for i, choice in enumerate(choices):
    solver.push()
    solver.add(choice)
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()