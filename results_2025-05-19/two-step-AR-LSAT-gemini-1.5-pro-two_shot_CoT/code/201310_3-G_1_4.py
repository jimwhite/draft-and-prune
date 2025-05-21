from z3 import *

# Define variables
U, V, W, X, Y, Z = 0, 1, 2, 3, 4, 5
band_at_slot = Array('band_at_slot', IntSort(), IntSort())
solver = Solver()
i = Int('i')
j = Int('j')

# Constraints
solver.add(ForAll([i], Implies(And(i >= 1, i <= 6), And(band_at_slot[i] >= 0, band_at_slot[i] <= 5)))) # Constraint 0
solver.add(Distinct([band_at_slot[i] for i in range(1, 7)])) # Constraint 1
solver.add(ForAll([i, j], Implies(And(i >= 1, i <= 6, j >= 1, j <= 6, band_at_slot[i] == V, band_at_slot[j] == Z), i < j))) # Constraint 2
solver.add(ForAll([i, j], Implies(And(i >= 1, i <= 6, j >= 1, j <= 6, band_at_slot[i] == W, band_at_slot[j] == X), i < j))) # Constraint 3
solver.add(ForAll([i, j], Implies(And(i >= 1, i <= 6, j >= 1, j <= 6, band_at_slot[i] == Z, band_at_slot[j] == X), i < j))) # Constraint 4
solver.add(Or(band_at_slot[4] == U, band_at_slot[5] == U, band_at_slot[6] == U)) # Constraint 5
solver.add(Or(band_at_slot[1] == Y, band_at_slot[2] == Y, band_at_slot[3] == Y)) # Constraint 6
solver.add(Exists([i], And(i >= 1, i <= 5, band_at_slot[i] == Z, band_at_slot[i+1] == W))) # Constraint 7


# Check answer choices
answer_choices = [
    Not(band_at_slot[5] == U),  # A
    Not(band_at_slot[1] == V),  # B
    Not(band_at_slot[5] == X),  # C
    Not(band_at_slot[2] == Y),  # D
    Not(band_at_slot[3] == Z)   # E
]

for i in range(len(answer_choices)):
    solver.push()
    solver.add(answer_choices[i])
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()