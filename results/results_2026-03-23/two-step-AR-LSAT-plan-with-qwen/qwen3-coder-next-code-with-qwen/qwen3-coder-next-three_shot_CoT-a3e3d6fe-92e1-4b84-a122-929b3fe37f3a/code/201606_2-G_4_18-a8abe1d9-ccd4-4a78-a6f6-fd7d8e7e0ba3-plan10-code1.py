from z3 import *

# Singer indices: 0=Kammer, 1=Lugo, 2=Trillo, 3=Waite, 4=Yoshida, 5=Zinn
singers = ["Kammer", "Lugo", "Trillo", "Waite", "Yoshida", "Zinn"]

# Position variables: pos[i] = position (1-6) of singer i
pos = [Int(f"pos_{i}") for i in range(6)]

# Base solver
solver = Solver()

# Domain constraints: positions 1-6
for i in range(6):
    solver.add(pos[i] >= 1, pos[i] <= 6)

# Distinctness constraint
solver.add(Distinct(pos))

# Recording constraints:
# - Only Kammer (0) and Lugo (1) are recorded
# - 4th audition cannot be recorded → neither Kammer nor Lugo at position 4
# - 5th audition must be recorded → either Kammer or Lugo at position 5
solver.add(pos[0] != 4, pos[1] != 4)
solver.add(Or(pos[0] == 5, pos[1] == 5))

# Waite constraint: Waite (3) must be earlier than both recorded auditions
solver.add(pos[3] < pos[0])
solver.add(pos[3] < pos[1])

# Kammer-Trillo constraint: Kammer (0) before Trillo (2)
solver.add(pos[0] < pos[2])

# Zinn-Yoshida constraint: Zinn (5) before Yoshida (4)
solver.add(pos[5] < pos[4])

# Answer choices
answer_choices = [
    ["Kammer", "Trillo", "Zinn", "Waite", "Lugo", "Yoshida"],
    ["Waite", "Kammer", "Yoshida", "Zinn", "Lugo", "Trillo"],
    ["Waite", "Lugo", "Kammer", "Trillo", "Zinn", "Yoshida"],
    ["Waite", "Zinn", "Kammer", "Trillo", "Lugo", "Yoshida"],
    ["Zinn", "Yoshida", "Waite", "Lugo", "Kammer", "Trillo"]
]

# Check each choice
valid_indices = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add position constraints based on the choice
    for i, singer in enumerate(choice):
        s_chk.add(pos[singers.index(singer)] == i + 1)
    
    if s_chk.check() == sat:
        valid_indices.append(idx)

print(valid_indices)