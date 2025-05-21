from z3 import *

# Entities (Band IDs)
U = 0
V = 1
W = 2
X = 3
Y = 4
Z = 5

# Variables
band_at_slot = Array('band_at_slot', IntSort(), IntSort())

# Solver
solver = Solver()

# Constraints
i = Int('i')
j = Int('j')

# Constraint 0 (Domain)
solver.add(ForAll([i], Implies(And(i >= 1, i <= 6), And(band_at_slot[i] >= 0, band_at_slot[i] <= 5))))

# Constraint 1 (Distinctness)
solver.add(Distinct([band_at_slot[i] for i in range(1, 7)]))

# Constraint 2 (V before Z)
solver.add(ForAll([i, j], Implies(And(i >= 1, i <= 6, j >= 1, j <= 6, band_at_slot[i] == V, band_at_slot[j] == Z), i < j)))

# Constraint 3 (W before X)
solver.add(ForAll([i, j], Implies(And(i >= 1, i <= 6, j >= 1, j <= 6, band_at_slot[i] == W, band_at_slot[j] == X), i < j)))

# Constraint 4 (Z before X)
solver.add(ForAll([i, j], Implies(And(i >= 1, i <= 6, j >= 1, j <= 6, band_at_slot[i] == Z, band_at_slot[j] == X), i < j)))

# Constraint 5 (U in last three)
solver.add(Or(band_at_slot[4] == U, band_at_slot[5] == U, band_at_slot[6] == U))

# Constraint 6 (Y in first three)
solver.add(Or(band_at_slot[1] == Y, band_at_slot[2] == Y, band_at_slot[3] == Y))


# Check answer choices
choices = [U, V, W, X, Z]
choice_names = ["Uneasy", "Vegemite", "Wellspring", "Xpert", "Zircon"]

for idx, choice in enumerate(choices):
    solver.push()
    solver.add(band_at_slot[5] == choice)
    if solver.check() == unsat:
        print(f"Option {chr(65 + idx)} is correct")
        exit()
    solver.pop()