from z3 import *

# Define constants for photographers and sections
F, G, H = 0, 1, 2
L, M, S = 0, 1, 2

# Define variables for photo assignments
L1, L2 = Int('L1'), Int('L2')
M1, M2 = Int('M1'), Int('M2')
S1, S2 = Int('S2'), Int('S2')

# Create solver
solver = Solver()

# Constraint 1: Domain
solver.add(And(L1 >= 0, L1 <= 2, L2 >= 0, L2 <= 2,
               M1 >= 0, M1 <= 2, M2 >= 0, M2 <= 2,
               S1 >= 0, S1 <= 2, S2 >= 0, S2 <= 2))

# Constraint 2: Distinctness within sections
solver.add(Distinct([L1, L2]))
solver.add(Distinct([M1, M2]))
solver.add(Distinct([S1, S2]))

# Constraint 4: Photographer photo counts
AtLeastOnePhoto = [Or(L1 == p, L2 == p, M1 == p, M2 == p, S1 == p, S2 == p) for p in range(3)]
AtMostThreePhotos = [AtMost(L1 == p, L2 == p, M1 == p, M2 == p, S1 == p, S2 == p, 3) for p in range(3)]
solver.add(AtLeastOnePhoto + AtMostThreePhotos)


# Constraint 5: Lifestyle/Metro overlap
solver.add(Or(L1 == M1, L1 == M2, L2 == M1, L2 == M2))

# Constraint 6: Hue in Lifestyle == Fuentes in Sports
solver.add(Sum([If(L1 == H, 1, 0), If(L2 == H, 1, 0)]) == Sum([If(S1 == F, 1, 0), If(S2 == F, 1, 0)]))

# Constraint 7: No Gagnon in Sports
solver.add(And(S1 != G, S2 != G))


for m1_val, m2_val in [(F, H), (H, F)]:  # Try both Metro assignments
    solver.push()
    solver.add(And(M1 == m1_val, M2 == m2_val))

    answer_choices = [
        And(L1 == F, L2 == F),  # A
        And(L1 == G, L2 == G),  # B
        Or(And(L1 == G, L2 == H), And(L1 == H, L2 == G)),  # C
        And(L1 == H, L2 == H),  # D
        And(S1 == F, S2 == F)   # E
    ]

    for i, choice in enumerate(answer_choices):
        solver.push()
        solver.add(choice)
        if solver.check() == sat:
            print(f"Option {chr(65 + i)} is correct")
            exit()
        solver.pop()

    solver.pop()