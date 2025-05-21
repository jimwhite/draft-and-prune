from z3 import *

# Variables
slot_U = Int('slot_U')
slot_V = Int('slot_V')
slot_W = Int('slot_W')
slot_X = Int('slot_X')
slot_Y = Int('slot_Y')
slot_Z = Int('slot_Z')

solver = Solver()

# Constraint 0 (Domain)
solver.add(And(1 <= slot_U, slot_U <= 6, 1 <= slot_V, slot_V <= 6, 1 <= slot_W, slot_W <= 6, 1 <= slot_X, slot_X <= 6, 1 <= slot_Y, slot_Y <= 6, 1 <= slot_Z, slot_Z <= 6))
# Constraint 1 (Distinctness)
solver.add(Distinct(slot_U, slot_V, slot_W, slot_X, slot_Y, slot_Z))
# Constraint 2 (V before Z)
solver.add(slot_V < slot_Z)
# Constraint 3 (W before X)
solver.add(slot_W < slot_X)
# Constraint 4 (Z before X)
solver.add(slot_Z < slot_X)
# Constraint 5 (U in last three)
solver.add(Or(slot_U == 4, slot_U == 5, slot_U == 6))
# Constraint 6 (Y in first three)
solver.add(Or(slot_Y == 1, slot_Y == 2, slot_Y == 3))
# Constraint 7 (Z immediately before W)
solver.add(slot_W == slot_Z + 1)

# Check answer choices
negations = [slot_U != 5, slot_V != 1, slot_X != 5, slot_Y != 2, slot_Z != 3]
for i, negation in enumerate(negations):
    solver.push()
    solver.add(negation)
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()