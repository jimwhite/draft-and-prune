from z3 import *

# Compositions and their indices
compositions = ["F", "H", "L", "O", "P", "R", "S", "T"]
comp_idx = {c: i for i, c in enumerate(compositions)}

# Position variables (1-indexed positions)
pos = [Int(f"pos_{c}") for c in compositions]

# Base solver
solver_base = Solver()

# Domain constraints: positions are distinct integers from 1 to 8
solver_base.add(Distinct(pos))
for i in range(8):
    solver_base.add(pos[i] >= 1, pos[i] <= 8)

# Condition 1: T is performed either immediately before F or immediately after R
T_idx = comp_idx["T"]
F_idx = comp_idx["F"]
R_idx = comp_idx["R"]
solver_base.add(Or(pos[T_idx] + 1 == pos[F_idx], pos[R_idx] + 1 == pos[T_idx]))

# Condition 2: At least two compositions between F and R
F_pos = pos[F_idx]
R_pos = pos[R_idx]
solver_base.add(Or(F_pos + 2 <= R_pos, R_pos + 2 <= F_pos))

# Condition 3: O is performed first or fifth
O_idx = comp_idx["O"]
solver_base.add(Or(pos[O_idx] == 1, pos[O_idx] == 5))

# Condition 4: Eighth composition is L or H
L_idx = comp_idx["L"]
H_idx = comp_idx["H"]
solver_base.add(Or(pos[L_idx] == 8, pos[H_idx] == 8))

# Condition 5: P before S
P_idx = comp_idx["P"]
S_idx = comp_idx["S"]
solver_base.add(pos[P_idx] < pos[S_idx])

# Condition 6: At least one composition between O and S
O_pos = pos[O_idx]
S_pos = pos[S_idx]
solver_base.add(Or(O_pos + 1 < S_pos, S_pos + 1 < O_pos))

# Answer choices
choices = [
    ["L", "P", "S", "R", "O", "T", "F", "H"],
    ["O", "T", "P", "F", "S", "H", "R", "L"],
    ["P", "T", "F", "S", "L", "R", "O", "H"],
    ["P", "T", "F", "S", "O", "R", "L", "H"],
    ["T", "F", "P", "R", "O", "L", "S", "H"]
]

# Check each choice
feasible_indices = []
for idx, choice in enumerate(choices):
    s = Solver()
    # Add base constraints
    s.add(solver_base.assertions())
    
    # Assert positions match the choice (choice[i] is performed at position i+1)
    for pos_val, comp in enumerate(choice, start=1):
        s.add(pos[comp_idx[comp]] == pos_val)
    
    if s.check() == sat:
        feasible_indices.append(idx)

# Print the index of the first feasible choice (as per question format)
print(feasible_indices[0] if feasible_indices else -1)