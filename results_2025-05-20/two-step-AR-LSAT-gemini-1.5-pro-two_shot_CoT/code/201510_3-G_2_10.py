from z3 import *

# Define constants for photographers and sections
F = 0
G = 1
H = 2

# Define the variable
photo_assignment = Array('photo_assignment', IntSort(), IntSort())

# Helper functions
def Count(indices, photographer_index):
    count = 0
    for i in indices:
        count += If(photo_assignment[i] == photographer_index, 1, 0)
    return count

def TotalCount(photographer_index):
    return Count(range(6), photographer_index)

# Create the solver and add constraints
solver = Solver()

# Constraint 1: Domain (Corrected: Use IntVal and range)
for i in range(6):
    solver.add(And(photo_assignment[i] >= 0, photo_assignment[i] < 3))

# Constraint 2: Photographer counts
solver.add(And(TotalCount(F) >= 1, TotalCount(F) <= 3))
solver.add(And(TotalCount(G) >= 1, TotalCount(G) <= 3))
solver.add(And(TotalCount(H) >= 1, TotalCount(H) <= 3))

# Constraint 3: Lifestyle/Metro overlap
solver.add(Or(
    And(Or(photo_assignment[0] == F, photo_assignment[1] == F), Or(photo_assignment[2] == F, photo_assignment[3] == F)),
    And(Or(photo_assignment[0] == G, photo_assignment[1] == G), Or(photo_assignment[2] == G, photo_assignment[3] == G)),
    And(Or(photo_assignment[0] == H, photo_assignment[1] == H), Or(photo_assignment[2] == H, photo_assignment[3] == H))
))

# Constraint 4: Hue/Fuentes balance
solver.add(Count([0, 1], H) == Count([4, 5], F))

# Constraint 5: No Gagnon in Sports
solver.add(And(photo_assignment[4] != G, photo_assignment[5] != G))


# Check answer choices
options = [
    [1, 1, 1],  # A: L=1, M=1, S=1
    [1, 0, 2],  # B: L=1, M=0, S=2
    [2, 0, 1],  # C: L=2, M=0, S=1
    [0, 1, 2],  # D: L=0, M=1, S=2
    [0, 2, 1]   # E: L=0, M=2, S=1
]

for i, option in enumerate(options):
    solver.push()
    solver.add(Count([0, 1], F) == option[0])
    solver.add(Count([2, 3], F) == option[1])
    solver.add(Count([4, 5], F) == option[2])
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()
