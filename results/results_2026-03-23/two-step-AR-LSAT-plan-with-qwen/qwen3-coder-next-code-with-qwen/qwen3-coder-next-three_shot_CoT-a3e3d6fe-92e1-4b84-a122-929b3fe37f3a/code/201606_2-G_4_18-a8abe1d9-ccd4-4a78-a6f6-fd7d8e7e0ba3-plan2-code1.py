from z3 import *

# Singer indices: Kammer=0, Lugo=1, Trillo=2, Waite=3, Yoshida=4, Zinn=5
singers = ["Kammer", "Lugo", "Trillo", "Waite", "Yoshida", "Zinn"]
pos = [Int(f"pos_{i}") for i in range(6)]

# Base solver
solver = Solver()

# Domain constraints: positions 1-6, all distinct
for i in range(6):
    solver.add(pos[i] >= 1, pos[i] <= 6)
solver.add(Distinct(*pos))

# Recorded auditions: Kammer (0) and Lugo (1)
# Position 4 cannot be recorded → not Kammer or Lugo
solver.add(pos[0] != 4, pos[1] != 4)

# Position 5 must be recorded → must be Kammer or Lugo
solver.add(Or(pos[0] == 5, pos[1] == 5))

# Waite (3) must be earlier than both recorded auditions
solver.add(pos[3] < pos[0], pos[3] < pos[1])

# Kammer (0) before Trillo (2)
solver.add(pos[0] < pos[2])

# Zinn (5) before Yoshida (4)
solver.add(pos[5] < pos[3])

# Answer choices
answer_choices = [
    ["Kammer", "Trillo", "Zinn", "Waite", "Lugo", "Yoshida"],
    ["Waite", "Kammer", "Yoshida", "Zinn", "Lugo", "Trillo"],
    ["Waite", "Lugo", "Kammer", "Trillo", "Zinn", "Yoshida"],
    ["Waite", "Zinn", "Kammer", "Trillo", "Lugo", "Yoshida"],
    ["Zinn", "Yoshida", "Waite", "Lugo", "Kammer", "Trillo"]
]

# Check each answer choice
valid_indices = []
for idx, order in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert exact positions based on the candidate order
    for i, singer in enumerate(order):
        s_chk.add(pos[singers.index(singer)] == i + 1)
    
    if s_chk.check() == sat:
        valid_indices.append(idx)

print(valid_indices)