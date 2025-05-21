from z3 import *

# Variables
slot_U, slot_V, slot_W, slot_X, slot_Y, slot_Z = Ints('slot_U slot_V slot_W slot_X slot_Y slot_Z')

# Solver
solver = Solver()

# Constraints
solver.add(And(slot_U >= 0, slot_U <= 5, slot_V >= 0, slot_V <= 5, slot_W >= 0, slot_W <= 5, slot_X >= 0, slot_X <= 5, slot_Y >= 0, slot_Y <= 5, slot_Z >= 0, slot_Z <= 5))
solver.add(Distinct(slot_U, slot_V, slot_W, slot_X, slot_Y, slot_Z))
solver.add(slot_V < slot_Z)
solver.add(slot_W < slot_X)
solver.add(slot_Z < slot_X)
solver.add(Or(slot_U == 3, slot_U == 4, slot_U == 5))
solver.add(Or(slot_Y == 0, slot_Y == 1, slot_Y == 2))

# Additional constraint from the question
solver.add(slot_Z < slot_Y)

# Check answer choices
slots = ["one", "two", "three", "four", "five", "six"]
for s in range(6):
    solver.push()
    solver.add(slot_W == s)
    if solver.check() == sat:
        print(f"Option {slots[s]} is correct")  # Corrected output format
        exit()
    solver.pop()