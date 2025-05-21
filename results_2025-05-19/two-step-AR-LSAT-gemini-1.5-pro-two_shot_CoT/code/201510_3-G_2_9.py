from z3 import *

# Define constants for photographers and sections
F = 0
G = 1
H = 2
L = 0
M = 1
S = 2

# Define the variable
photo_assignment = Array('photo_assignment', IntSort(), IntSort())

# Create the solver
solver = Solver()

# Constraint 1: Two photos per section
s = Int('s')
solver.add(ForAll([s], Implies(And(s >= 0, s <= 2), Sum([If(photo_assignment[i] == s, 1, 0) for i in range(2)]) + Sum([If(photo_assignment[i] == s, 1, 0) for i in range(2, 4)]) + Sum([If(photo_assignment[i] == s, 1, 0) for i in range(4, 6)]) == 2)))


# Constraint 2: At least one and at most three photos per photographer
p = Int('p')
solver.add(ForAll([p], Implies(And(p >= 0, p <= 2), And(Sum([If(photo_assignment[i] == p, 1, 0) for i in range(6)]) >= 1, Sum([If(photo_assignment[i] == p, 1, 0) for i in range(6)]) <= 3))))

# Constraint 3: Lifestyle/Metro overlap
solver.add(Or(
    And(photo_assignment[0] == photo_assignment[2], photo_assignment[0] != photo_assignment[3]),
    And(photo_assignment[0] == photo_assignment[3], photo_assignment[0] != photo_assignment[2]),
    And(photo_assignment[1] == photo_assignment[2], photo_assignment[1] != photo_assignment[3]),
    And(photo_assignment[1] == photo_assignment[3], photo_assignment[1] != photo_assignment[2])
))

# Constraint 4: Hue in Lifestyle / Fuentes in Sports
solver.add(Sum([If(photo_assignment[i] == H, 1, 0) for i in range(2)]) == Sum([If(photo_assignment[i] == F, 1, 0) for i in range(4, 6)]))

# Constraint 5: No Gagnon in Sports
solver.add(Not(Or(photo_assignment[4] == G, photo_assignment[5] == G)))

# Constraint 6: Given condition - Gagnon and Hue in Lifestyle
solver.add(photo_assignment[0] == G)
solver.add(photo_assignment[1] == H)

# Check answer choices
answer_choices = [
    Sum([If(photo_assignment[i] == F, 1, 0) for i in range(2, 4)]) == 1,  # A
    Sum([If(photo_assignment[i] == G, 1, 0) for i in range(2, 4)]) == 1,  # B
    And(photo_assignment[2] == G, photo_assignment[3] == G),  # C
    Sum([If(photo_assignment[i] == H, 1, 0) for i in range(4, 6)]) == 1,  # D
    And(photo_assignment[4] == H, photo_assignment[5] == H)  # E
]

for i, choice in enumerate(answer_choices):
    solver.push()
    solver.add(Not(choice))
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()