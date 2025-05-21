from z3 import *

# Variables
photo = [Int('photo_%i' % i) for i in range(6)]

solver = Solver()

# Constraints
# Constraint 1 (Two photos per section)
solver.add(Sum([If(photo[i] == 0, 1, 0) for i in range(2)]) == 2)  # Lifestyle
solver.add(Sum([If(photo[i] == 1, 1, 0) for i in range(2, 4)]) == 2)  # Metro
solver.add(Sum([If(photo[i] == 2, 1, 0) for i in range(4, 6)]) == 2)  # Sports

# Constraint 2 (At least one and at most three photos per photographer)
# Corrected: Separate the combined inequality into two separate inequalities
solver.add(Sum([If(photo[i] == 0, 1, 0) for i in range(6)]) >= 1)  # Fuentes
solver.add(Sum([If(photo[i] == 0, 1, 0) for i in range(6)]) <= 3)  # Fuentes
solver.add(Sum([If(photo[i] == 1, 1, 0) for i in range(6)]) >= 1)  # Gagnon
solver.add(Sum([If(photo[i] == 1, 1, 0) for i in range(6)]) <= 3)  # Gagnon
solver.add(Sum([If(photo[i] == 2, 1, 0) for i in range(6)]) >= 1)  # Hue
solver.add(Sum([If(photo[i] == 2, 1, 0) for i in range(6)]) <= 3)  # Hue

# Constraint 3 (Lifestyle/Metro overlap)
solver.add(Or(photo[0] == photo[2], photo[0] == photo[3], photo[1] == photo[2], photo[1] == photo[3]))

# Constraint 4 (Hue in Lifestyle and Fuentes in Sports)
solver.add(Sum([If(photo[i] == 2, 1, 0) for i in range(2)]) == Sum([If(photo[i] == 0, 1, 0) for i in range(4, 6)]))

# Constraint 5 (No Gagnon in Sports)
solver.add(And(photo[4] != 1, photo[5] != 1))

# Constraint 6 (Two Gagnon photos in one section)
solver.add(Or(And(photo[0] == 1, photo[1] == 1), And(photo[2] == 1, photo[3] == 1)))


# Check answer choices
choices = [
    And(photo[0] == 2, photo[1] == 2),  # A
    Or(And(photo[0] == 0, photo[1] == 2), And(photo[0] == 2, photo[1] == 0)),  # B
    And(photo[2] == 0, photo[3] == 0),  # C
    Or(And(photo[2] == 1, photo[3] == 2), And(photo[2] == 2, photo[3] == 1)),  # D
    And(photo[4] == 2, photo[5] == 2)  # E
]

for i, choice in enumerate(choices):
    solver.push()
    solver.add(choice)
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()
