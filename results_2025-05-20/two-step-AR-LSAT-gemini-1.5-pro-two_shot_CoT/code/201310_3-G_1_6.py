from z3 import *

# Variables
slot_U = Int('slot_U')
slot_V = Int('slot_V')
slot_W = Int('slot_W')
slot_X = Int('slot_X')
slot_Y = Int('slot_Y')
slot_Z = Int('slot_Z')

solver = Solver()

# Base Constraints
solver.add(And(slot_U >= 1, slot_U <= 6))
solver.add(And(slot_V >= 1, slot_V <= 6))
solver.add(And(slot_W >= 1, slot_W <= 6))
solver.add(And(slot_X >= 1, slot_X <= 6))
solver.add(And(slot_Y >= 1, slot_Y <= 6))
solver.add(And(slot_Z >= 1, slot_Z <= 6))

solver.add(Distinct(slot_U, slot_V, slot_W, slot_X, slot_Y, slot_Z))

solver.add(slot_V < slot_Z)
solver.add(slot_W < slot_X)
solver.add(slot_Z < slot_X)
solver.add(Or(slot_U == 4, slot_U == 5, slot_U == 6))
solver.add(Or(slot_Y == 1, slot_Y == 2, slot_Y == 3))

# Given Condition
solver.add(slot_X == slot_W + 1)

# Answer Choices
choices = [
    (slot_U == 5, 'A'),
    (slot_V == 3, 'B'),
    (slot_W == 3, 'C'),
    (slot_Z == 2, 'D'),
    (slot_Z == 4, 'E')
]

for choice, option in choices:
    solver.push()
    solver.add(choice)
    if solver.check() == sat:
        print(f"Option {option} is correct")
        exit()
    solver.pop()