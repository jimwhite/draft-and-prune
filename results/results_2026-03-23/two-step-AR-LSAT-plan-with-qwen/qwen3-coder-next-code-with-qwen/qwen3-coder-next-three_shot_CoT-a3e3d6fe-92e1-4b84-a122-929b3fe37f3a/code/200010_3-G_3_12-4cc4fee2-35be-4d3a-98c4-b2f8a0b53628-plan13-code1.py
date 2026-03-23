from z3 import *

# Compositions
compositions = ['F', 'H', 'L', 'O', 'P', 'R', 'S', 'T']
comp_idx = {c: i for i, c in enumerate(compositions)}

# Create position variables
pos = [Int(f"pos_{c}") for c in compositions]

# Base solver
solver = Solver()

# Domain constraints: positions are 0..7 (representing 1st to 8th)
solver.add(Distinct(pos))
for i in range(8):
    solver.add(pos[i] >= 0, pos[i] <= 7)

# T-F-R adjacency constraint: T immediately before F OR T immediately after R
T_before_F = (pos[comp_idx['T']] == pos[comp_idx['F']] - 1)
T_after_R = (pos[comp_idx['R']] == pos[comp_idx['T']] - 1)
solver.add(Or(T_before_F, T_after_R))

# At least two between F and R
F_before_R = (pos[comp_idx['F']] + 2 < pos[comp_idx['R']])
R_before_F = (pos[comp_idx['R']] + 2 < pos[comp_idx['F']])
solver.add(Or(F_before_R, R_before_F))

# O is first or fifth (positions 0 or 4)
solver.add(Or(pos[comp_idx['O']] == 0, pos[comp_idx['O']] == 4))

# Eighth composition is L or H
# In our pos array, position i corresponds to index i (0-based)
# So we need: order[7] == 'L' or 'H'
# But we have pos variables, so we need to express: 
#   (pos[comp_idx['L']] == 7) OR (pos[comp_idx['H']] == 7)
solver.add(Or(pos[comp_idx['L']] == 7, pos[comp_idx['H']] == 7))

# P before S
solver.add(pos[comp_idx['P']] < pos[comp_idx['S']])

# At least one between O and S (|pos_O - pos_S| >= 2)
solver.add(Abs(pos[comp_idx['O']] - pos[comp_idx['S']]) >= 2)

# Answer choices
choices = [
    ['L', 'P', 'S', 'R', 'O', 'T', 'F', 'H'],
    ['O', 'T', 'P', 'F', 'S', 'H', 'R', 'L'],
    ['P', 'T', 'F', 'S', 'L', 'R', 'O', 'H'],
    ['P', 'T', 'F', 'S', 'O', 'R', 'L', 'H'],
    ['T', 'F', 'P', 'R', 'O', 'L', 'S', 'H']
]

# Check each choice
valid_indices = []
for idx, choice in enumerate(choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assign positions based on the choice list
    for i, comp in enumerate(choice):
        s_chk.add(pos[comp_idx[comp]] == i)
    
    if s_chk.check() == sat:
        valid_indices.append(idx)

print(valid_indices)