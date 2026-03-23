from z3 import *

# Photographer indices: 0-Fuentes, 1-Gagnon, 2-Hue
# Section indices: 0-Lifestyle, 1-Metro, 2-Sports

# f[i][j] = number of photographs by photographer i in section j
f = [[Int(f"f_{i}_{j}") for j in range(3)] for i in range(3)]

# Base solver
solver = Solver()

# Per-section totals: exactly 2 photos per section
solver.add(f[0][0] + f[1][0] + f[2][0] == 2)  # Lifestyle
solver.add(f[0][1] + f[1][1] + f[2][1] == 2)  # Metro
solver.add(f[0][2] + f[1][2] + f[2][2] == 2)  # Sports

# Non-negativity and integrality (values between 0 and 2)
for i in range(3):
    for j in range(3):
        solver.add(f[i][j] >= 0, f[i][j] <= 2)

# Global photographer counts: at least 1, at most 3
for i in range(3):
    total = f[i][0] + f[i][1] + f[i][2]
    solver.add(total >= 1, total <= 3)

# Gagnon constraint: no photos in Sports
solver.add(f[1][2] == 0)

# Cross-section constraint: at least one Lifestyle photographer appears in Metro
solver.add(Or(
    And(f[0][0] > 0, f[0][1] > 0),
    And(f[1][0] > 0, f[1][1] > 0),
    And(f[2][0] > 0, f[2][1] > 0)
))

# Hue-Lifestyle = Fuentes-Sports constraint
solver.add(f[2][0] == f[0][2])

# Given condition: one Lifestyle photo by Fuentes and one by Hue
solver.add(f[0][0] == 1, f[2][0] == 1)

# Answer choices
answer_choices = [
    "Both Metro by Fuentes",      # 0: f[0][1] == 2
    "Both Metro by Gagnon",       # 1: f[1][1] == 2
    "Exactly one Metro by Hue",   # 2: f[2][1] == 1
    "Both Sports by Hue",         # 3: f[2][2] == 2
    "Neither Sports by Hue"       # 4: f[2][2] == 0
]

# Check each answer choice
answer_index_list = []
for idx, condition in enumerate(answer_choices):
    s_chk = Solver()
    # Add all base constraints plus given condition
    for a in solver.assertions():
        s_chk.add(a)
    
    # Add specific condition for this choice
    if idx == 0:  # Both Metro by Fuentes
        s_chk.add(f[0][1] == 2)
    elif idx == 1:  # Both Metro by Gagnon
        s_chk.add(f[1][1] == 2)
    elif idx == 2:  # Exactly one Metro by Hue
        s_chk.add(f[2][1] == 1)
    elif idx == 3:  # Both Sports by Hue
        s_chk.add(f[2][2] == 2)
    elif idx == 4:  # Neither Sports by Hue
        s_chk.add(f[2][2] == 0)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)