from z3 import *

# Compositions indices
(F, H, L, O, P, R, S, T) = range(8)

# Create order variables: order[k] is the composition at position k (0-indexed, positions 0-7)
order = [Int(f"order_{k}") for k in range(8)]

# Base solver
solver = Solver()

# Permutation constraint: all positions must be distinct and cover 0-7
solver.add(Distinct(order))
for k in range(8):
    solver.add(Or(*[order[k] == i for i in range(8)]))

# T-F-R adjacency constraint: T is performed either immediately before F or immediately after R
pos = {comp: Int(f"pos_{comp}") for comp in range(8)}
for comp in range(8):
    solver.add(pos[comp] == Sum([If(order[k] == comp, k + 1, 0) for k in range(8)]))

# T immediately before F: pos_T + 1 == pos_F
# OR T immediately after R: pos_R + 1 == pos_T
solver.add(Or(pos[T] + 1 == pos[F], pos[R] + 1 == pos[T]))

# At least two compositions between F and R: |pos_F - pos_R| >= 3
solver.add(Or(pos[F] <= pos[R] - 3, pos[F] >= pos[R] + 3))

# O is performed either first or fifth: pos_O == 1 or pos_O == 5
solver.add(Or(pos[O] == 1, pos[O] == 5))

# Eighth composition is either L or H: position 8 (index 7 in order array) must be L or H
solver.add(Or(order[7] == L, order[7] == H))

# P before S: pos_P < pos_S
solver.add(pos[P] < pos[S])

# At least one composition between O and S: |pos_O - pos_S| >= 2
solver.add(Or(pos[O] <= pos[S] - 2, pos[O] >= pos[S] + 2))

# Answer choices
choices = [
    ["L", "P", "S", "R", "O", "T", "F", "H"],
    ["O", "T", "P", "F", "S", "H", "R", "L"],
    ["P", "T", "F", "S", "L", "R", "O", "H"],
    ["P", "T", "F", "S", "O", "R", "L", "H"],
    ["T", "F", "P", "R", "O", "L", "S", "H"]
]

# Map composition names to indices
comp_map = {"F": F, "H": H, "L": L, "O": O, "P": P, "R": R, "S": S, "T": T}

# Check each choice
valid_indices = []
for idx, choice in enumerate(choices):
    s_chk = Solver()
    # Add all base constraints
    for a in solver.assertions():
        s_chk.add(a)
    
    # Add specific ordering constraints from the choice
    for k, comp_name in enumerate(choice):
        s_chk.add(order[k] == comp_map[comp_name])
    
    if s_chk.check() == sat:
        valid_indices.append(idx)

print(valid_indices)