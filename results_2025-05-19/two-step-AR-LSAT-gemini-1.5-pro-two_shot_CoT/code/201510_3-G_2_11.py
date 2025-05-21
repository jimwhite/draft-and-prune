from z3 import *

# Variables
section_counts = [[Int('section_%s_%s' % (s, p)) for p in range(3)] for s in range(3)]

# Solver
solver = Solver()

# Constraints
# Constraint 1: Two photos per section
for s in range(3):
    solver.add(Sum(section_counts[s]) == 2)

# Constraint 2: Photographer photo counts
for p in range(3):
    solver.add(And(Sum([section_counts[s][p] for s in range(3)]) >= 1, Sum([section_counts[s][p] for s in range(3)]) <= 3))

# Constraint 3: Lifestyle/Metro overlap
solver.add(Or([And(section_counts[0][p] >= 1, section_counts[1][p] >= 1) for p in range(3)]))

# Constraint 4: Hue/Fuentes equality
solver.add(section_counts[0][2] == section_counts[2][0])

# Constraint 5: No Gagnon in Sports
solver.add(section_counts[2][1] == 0)

# Constraint 6: Initial Lifestyle assignments
solver.add(section_counts[0][0] == 1)
solver.add(section_counts[0][2] == 1)

# Additional constraints for non-negativity
for i in range(3):
    for j in range(3):
        solver.add(section_counts[i][j] >= 0)


# Check answer choices
answer_choices = [
    (section_counts[1][0] == 2, 'A'),
    (section_counts[1][1] == 2, 'B'),
    (section_counts[1][2] == 1, 'C'),
    (section_counts[2][2] == 2, 'D'),
    (section_counts[2][2] == 0, 'E')
]

for constraint, option in answer_choices:
    solver.push()
    solver.add(constraint)
    if solver.check() == sat:
        print(f"Option {option} is correct")
        exit()
    solver.pop()
