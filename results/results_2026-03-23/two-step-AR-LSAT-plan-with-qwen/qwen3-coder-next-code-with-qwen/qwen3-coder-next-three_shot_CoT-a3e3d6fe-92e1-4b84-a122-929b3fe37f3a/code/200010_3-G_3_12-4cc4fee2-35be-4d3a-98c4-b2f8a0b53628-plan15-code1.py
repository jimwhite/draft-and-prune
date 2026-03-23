from z3 import *

# Composition indices: F=0, H=1, L=2, O=3, P=4, R=5, S=6, T=7
compositions = ["F", "H", "L", "O", "P", "R", "S", "T"]
comp_idx = {c: i for i, c in enumerate(compositions)}

# Position variables (1-8)
pos = [Int(f"pos_{c}") for c in compositions]

# Base solver
solver = Solver()

# Domain and uniqueness constraints
for i in range(8):
    solver.add(pos[i] >= 1, pos[i] <= 8)
solver.add(Distinct(pos))

# T-F-R adjacency constraint: T immediately before F OR T immediately after R
solver.add(Or(pos[7] == pos[0] - 1, pos[7] == pos[5] + 1))

# Spacing constraint for F and R: at least two between them
solver.add(Or(pos[0] <= pos[5] - 3, pos[5] <= pos[0] - 3))

# O constraint: first or fifth
solver.add(Or(pos[3] == 1, pos[3] == 5))

# Eighth position constraint: L or H is eighth
solver.add(Or(pos[2] == 8, pos[1] == 8))

# P-before-S constraint
solver.add(pos[4] < pos[6])

# O-S interleaving: at least one between them
solver.add(Abs(pos[3] - pos[6]) >= 2)

# Answer choices
answer_choices = [
    "L, P, S, R, O, T, F, H",
    "O, T, P, F, S, H, R, L",
    "P, T, F, S, L, R, O, H",
    "P, T, F, S, O, R, L, H",
    "T, F, P, R, O, L, S, H"
]

# Parse each choice and check
for idx, choice in enumerate(answer_choices):
    order = [c.strip() for c in choice.split(",")]
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert positions based on the order (1-indexed)
    for i, comp in enumerate(order):
        s_chk.add(pos[comp_idx[comp]] == i + 1)
    
    if s_chk.check() == sat:
        print(choice)
        break