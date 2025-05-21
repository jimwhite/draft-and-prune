from z3 import *

# 1. Define compositions and map them to integer IDs
F = 0
H = 1
L = 2
O = 3
P = 4
R = 5
S = 6
T = 7

# 2. Declare integer variables for positions
pos_F = Int('pos_F')
pos_H = Int('pos_H')
pos_L = Int('pos_L')
pos_O = Int('pos_O')
pos_P = Int('pos_P')
pos_R = Int('pos_R')
pos_S = Int('pos_S')
pos_T = Int('pos_T')

# 3. Create a solver and add constraints
solver = Solver()

# Each position variable must be between 0 and 7
for pos in [pos_F, pos_H, pos_L, pos_O, pos_P, pos_R, pos_S, pos_T]:
    solver.add(And(pos >= 0, pos < 8))

# All position variables must be distinct
solver.add(Distinct([pos_F, pos_H, pos_L, pos_O, pos_P, pos_R, pos_S, pos_T]))

# T is performed either immediately before F or immediately after R
solver.add(Or(pos_T == pos_F - 1, pos_T == pos_R + 1))

# At least two compositions are performed either after F and before R, or after R and before F
solver.add(Or(pos_R - pos_F >= 3, pos_F - pos_R >= 3))

# O is performed either first or fifth
solver.add(Or(pos_O == 0, pos_O == 4))

# The eighth composition performed is either L or H
solver.add(Or(pos_L == 7, pos_H == 7))

# P is performed at some time before S
solver.add(pos_P < pos_S)

# At least one composition is performed either after O and before S, or after S and before O
solver.add(Or(pos_S - pos_O >= 2, pos_O - pos_S >= 2))

# 4. Iterate through the answer choices
choices = [
    "L, P, S, R, O, T, F, H",
    "O, T, P, F, S, H, R, L",
    "P, T, F, S, L, R, O, H",
    "P, T, F, S, O, R, L, H",
    "T, F, P, R, O, L, S, H"
]

composition_map = {'F': pos_F, 'H': pos_H, 'L': pos_L, 'O': pos_O, 'P': pos_P, 'R': pos_R, 'S': pos_S, 'T': pos_T}

for i, choice in enumerate(choices):
    solver.push()
    compositions = choice.split(', ')
    for j, comp in enumerate(compositions):
        solver.add(composition_map[comp] == j)
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()