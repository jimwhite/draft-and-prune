from z3 import *

# Define variables
O, P, R, S, T = 0, 1, 2, 3, 4
G, H = 0, 1
lecture_bird = Array('lecture_bird', IntSort(), IntSort())
lecture_location = Array('lecture_location', IntSort(), IntSort())

solver = Solver()

# Constraint 1: Bird Uniqueness
solver.add(Distinct([lecture_bird[i] for i in range(1, 6)]))

# Constraint 2: First Lecture Location
solver.add(lecture_location[1] == G)

# Constraint 3: Fourth Lecture Location
solver.add(lecture_location[4] == H)

# Constraint 4: Three Lectures in Gladwyn
solver.add(Sum([If(lecture_location[i] == G, 1, 0) for i in range(1, 6)]) == 3)

# Constraint 5: Sandpipers in Howard
# Use Implies to represent the relationship between bird and location
for i in range(1, 6):
    solver.add(Implies(lecture_bird[i] == S, lecture_location[i] == H))

# Constraint 6: Sandpipers before Oystercatchers
# Use Implies to represent the ordering constraint
for i in range(1, 6):
    for j in range(i + 1, 6):
        solver.add(Implies(lecture_bird[i] == O, lecture_bird[j] != S))
        solver.add(Implies(lecture_bird[i] == S, lecture_bird[j] != O))


# Constraint 7: Terns before Petrels
for i in range(1, 6):
    for j in range(i + 1, 6):
        solver.add(Implies(lecture_bird[i] == P, lecture_bird[j] != T))
        solver.add(Implies(lecture_bird[i] == T, lecture_bird[j] != P))

# Constraint 8: Petrels in Gladwyn
for i in range(1, 6):
    solver.add(Implies(lecture_bird[i] == P, lecture_location[i] == G))


# Check answer choices
choices = [
    (O, G),  # A
    (P, H),  # B
    (R, H),  # C
    (S, H),  # D
    (T, G)   # E
]

for i, (bird, location) in enumerate(choices):
    solver.push()
    solver.add(lecture_bird[5] == bird)
    solver.add(lecture_location[5] == location)
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()
