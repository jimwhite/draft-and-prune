from z3 import *

# Photographer indices: Fuentes=0, Gagnon=1, Hue=2
# Section indices: Lifestyle=0, Metro=1, Sports=2

# Create count variables: count[section][photographer]
count = [[Int(f"count_{s}_{p}") for p in range(3)] for s in range(3)]

# Base solver
solver = Solver()

# Per-section cardinality constraints: each section has exactly 2 photographs
for s in range(3):
    solver.add(count[s][0] + count[s][1] + count[s][2] == 2)

# Total-photograph-per-photographer constraints: each photographer has 1 to 3 photos
for p in range(3):
    total = count[0][p] + count[1][p] + count[2][p]
    solver.add(total >= 1, total <= 3)

# Gagnon-in-Sports-prohibited constraint
solver.add(count[2][1] == 0)

# Lifestyle-Metro overlap constraint: at least one photographer appears in both
shared = [Bool(f"shared_{p}") for p in range(3)]
for p in range(3):
    solver.add(shared[p] == And(count[0][p] > 0, count[1][p] > 0))
solver.add(Or(shared))

# Hue-in-Lifestyle = Fuentes-in-Sports constraint
solver.add(count[0][2] == count[2][0])

# Given condition: Lifestyle has one Fuentes and one Hue
solver.add(count[0][0] == 1)  # Fuentes in Lifestyle
solver.add(count[0][2] == 1)  # Hue in Lifestyle
# This implies count[0][1] == 0 (Gagnon in Lifestyle), but it's already enforced by the section constraint

# Answer choices
answer_choices = [
    count[1][0] == 2,  # Both Metro by Fuentes
    count[1][1] == 2,  # Both Metro by Gagnon
    count[1][2] == 1,  # Exactly one Metro by Hue
    count[2][2] == 2,  # Both Sports by Hue
    count[2][2] == 0   # Neither Sports by Hue
]

# Check each answer choice
answer_index_list = []
for idx, constraint in enumerate(answer_choices):
    s_chk = Solver()
    # Add all base constraints
    for assertion in solver.assertions():
        s_chk.add(assertion)
    # Add the choice-specific constraint
    s_chk.add(constraint)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)