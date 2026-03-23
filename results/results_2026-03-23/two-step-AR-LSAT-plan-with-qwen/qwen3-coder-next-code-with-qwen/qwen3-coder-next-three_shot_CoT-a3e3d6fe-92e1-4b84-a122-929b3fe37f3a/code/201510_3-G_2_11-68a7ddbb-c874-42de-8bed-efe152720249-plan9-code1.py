from z3 import *

# Photographer indices: 0=Fuentes, 1=Gagnon, 2=Hue
# Section indices: 0=Lifestyle, 1=Metro, 2=Sports

# Create count variables: count[photographer][section]
count = [[Int(f"count_{i}_{j}") for j in range(3)] for i in range(3)]

# Base solver
solver = Solver()

# Global sum constraint: total photographs = 6
solver.add(Sum([count[i][j] for i in range(3) for j in range(3)]) == 6)

# Per-section constraint: each section has exactly 2 photos
for j in range(3):
    solver.add(Sum([count[i][j] for i in range(3)]) == 2)

# Per-photographer constraints: each photographer has 1 to 3 photos
for i in range(3):
    total = Sum([count[i][j] for j in range(3)])
    solver.add(total >= 1, total <= 3)

# Gagnon constraint: no photos in Sports
solver.add(count[1][2] == 0)

# Lifestyle/Metro overlap constraint: at least one photographer appears in both
overlap_constraint = Or(
    And(count[0][0] > 0, count[0][1] > 0),
    And(count[1][0] > 0, count[1][1] > 0),
    And(count[2][0] > 0, count[2][1] > 0)
)
solver.add(overlap_constraint)

# Hue/Fuentes correspondence constraint: count[2][0] == count[0][2]
solver.add(count[2][0] == count[0][2])

# Given condition: Lifestyle has exactly one Fuentes and one Hue
solver.add(count[0][0] == 1, count[2][0] == 1)

# Since Lifestyle has exactly 2 photos and we have 1 Fuentes + 1 Hue,
# Gagnon count in Lifestyle must be 0
solver.add(count[1][0] == 0)

# From correspondence: count[0][2] = count[2][0] = 1
# So Sports has exactly one Fuentes photo

# Answer choices:
# A: Both Metro by Fuentes -> count[0][1] == 2
# B: Both Metro by Gagnon -> count[1][1] == 2 and count[0][1] == 0 and count[2][1] == 0
# C: Exactly one Metro by Hue -> count[2][1] == 1
# D: Both Sports by Hue -> count[2][2] == 2
# E: Neither Sport by Hue -> count[2][2] == 0

answer_choices = [
    lambda: And(count[0][1] == 2),
    lambda: And(count[1][1] == 2, count[0][1] == 0, count[2][1] == 0),
    lambda: And(count[2][1] == 1),
    lambda: And(count[2][2] == 2),
    lambda: And(count[2][2] == 0)
]

answer_index_list = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    # Add all base constraints plus the Lifestyle condition
    for assertion in solver.assertions():
        s_chk.add(assertion)
    
    # Add the specific choice constraint
    s_chk.add(choice())
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)