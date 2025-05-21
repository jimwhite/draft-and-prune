from z3 import *

# Define constants for bands
U = 0
V = 1
W = 2
X = 3
Y = 4
Z = 5

# Define the variable
slot_of_band = Array('slot_of_band', IntSort(), IntSort())

# Create the solver
solver = Solver()

# Constraint 0 (Domain)
b = Int('b')
solver.add(ForAll([b], And(slot_of_band[b] >= 0, slot_of_band[b] < 6)))

# Constraint 1 (Distinctness)
solver.add(Distinct([slot_of_band[b] for b in range(6)]))

# Constraint 2 (V before Z)
solver.add(slot_of_band[V] < slot_of_band[Z])

# Constraint 3 (W before X)
solver.add(slot_of_band[W] < slot_of_band[X])

# Constraint 4 (Z before X)
solver.add(slot_of_band[Z] < slot_of_band[X])

# Constraint 5 (U in last three)
solver.add(Or(slot_of_band[U] == 3, slot_of_band[U] == 4, slot_of_band[U] == 5))

# Constraint 6 (Y in first three)
solver.add(Or(slot_of_band[Y] == 0, slot_of_band[Y] == 1, slot_of_band[Y] == 2))

# Constraint 7 (Z before Y)
solver.add(slot_of_band[Z] < slot_of_band[Y])

# Check answer choices
answer_choices = [1, 2, 3, 4, 5]  # Corresponding to "two", "three", "four", "five", "six"
option_letter = 'A'

for slot_value in answer_choices:
    solver.push()
    solver.add(slot_of_band[W] == slot_value)
    if solver.check() == sat:
        print(f"Option {option_letter} is correct")
        exit()
    solver.pop()
    option_letter = chr(ord(option_letter) + 1)