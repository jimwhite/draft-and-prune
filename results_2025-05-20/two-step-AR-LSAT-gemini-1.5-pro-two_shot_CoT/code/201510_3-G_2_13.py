from z3 import *

# Variables
L1_p = Int('L1_p')
L2_p = Int('L2_p')
M1_p = Int('M1_p')
M2_p = Int('M2_p')
S1_p = Int('S1_p')
S2_p = Int('S2_p')

solver = Solver()

# Constraints on photographer values
all_photo_vars = [L1_p, L2_p, M1_p, M2_p, S1_p, S2_p]
for var in all_photo_vars:
    solver.add(And(var >= 0, var <= 2))

# Derived Counts
count_F = Sum([If(var == 0, 1, 0) for var in all_photo_vars])
count_G = Sum([If(var == 1, 1, 0) for var in all_photo_vars])
count_H = Sum([If(var == 2, 1, 0) for var in all_photo_vars])
count_H_L = Sum([If(var == 2, 1, 0) for var in [L1_p, L2_p]])
count_F_S = Sum([If(var == 0, 1, 0) for var in [S1_p, S2_p]])

# Base Constraints
solver.add(And(count_F >= 1, count_F <= 3))
solver.add(And(count_G >= 1, count_G <= 3))
solver.add(And(count_H >= 1, count_H <= 3))
solver.add(Or(And(M1_p == 0, M2_p == 2), And(M1_p == 2, M2_p == 0)))
solver.add(Or(L1_p == 0, L1_p == 2, L2_p == 0, L2_p == 2))  # At least one L by F or H
solver.add(count_H_L == count_F_S)
solver.add(And(S1_p != 1, S2_p != 1))

# Answer Choices
options = [
    And(L1_p == 0, L2_p == 0),  # A
    And(L1_p == 1, L2_p == 1),  # B
    Or(And(L1_p == 1, L2_p == 2), And(L1_p == 2, L2_p == 1)),  # C
    And(L1_p == 2, L2_p == 2),  # D
    And(S1_p == 0, S2_p == 0)   # E
]

for i, option in enumerate(options):
    solver.push()
    solver.add(option)
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()