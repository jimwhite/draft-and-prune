from z3 import *

# Variables
photo_assignment = [[Int('p_%s_%s' % (s,p)) for p in range(2)] for s in range(3)]
photo_counts = [Int('c_%s' % p) for p in range(3)]

# Solver
solver = Solver()

# Constraints

# Constraint 1 (Two photos per section)
for s in range(3):
    solver.add(Sum([If(photo_assignment[s][p] == f, 1, 0) for p in range(2) for f in range(3)]) == 2)

# Constraint 2 (Total six photos)
solver.add(Sum(photo_counts) == 6)

# Constraint 3 (Photographer photo limits)
solver.add(And([And(photo_counts[p] >= 1, photo_counts[p] <= 3) for p in range(3)]))

# Constraint 4 (Lifestyle/Metro overlap)
solver.add(Or(photo_assignment[0][0] == photo_assignment[1][0],
               photo_assignment[0][0] == photo_assignment[1][1],
               photo_assignment[0][1] == photo_assignment[1][0],
               photo_assignment[0][1] == photo_assignment[1][1]))

# Constraint 5 (Hue/Fuentes balance)
solver.add(Sum([If(photo_assignment[0][p] == 2, 1, 0) for p in range(2)]) == Sum([If(photo_assignment[2][p] == 0, 1, 0) for p in range(2)]))

# Constraint 6 (No Gagnon in Sports)
solver.add(And(Not(photo_assignment[2][0] == 1), Not(photo_assignment[2][1] == 1)))

# Constraint 7 (Both Lifestyle by Hue)
solver.add(And(photo_assignment[0][0] == 2, photo_assignment[0][1] == 2))

# Constraint 8 (Photo counts definition)
for f in range(3):
    solver.add(photo_counts[f] == Sum([If(photo_assignment[s][p] == f, 1, 0) for s in range(3) for p in range(2)]))



# Check answer choices
answer_choices = [
    photo_counts[0] == 1,  # A
    photo_counts[0] == 3,  # B
    photo_counts[1] == 1,  # C
    photo_counts[1] == 2,  # D
    photo_counts[2] == 2   # E
]

for i, choice in enumerate(answer_choices):
    solver.push()
    solver.add(choice)
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()
