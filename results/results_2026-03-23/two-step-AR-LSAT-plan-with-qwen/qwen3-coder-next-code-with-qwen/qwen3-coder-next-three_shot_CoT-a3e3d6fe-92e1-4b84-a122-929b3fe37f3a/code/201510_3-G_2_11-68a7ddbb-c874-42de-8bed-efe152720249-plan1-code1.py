from z3 import *

# Photographer indices: 0-Fuentes, 1-Gagnon, 2-Hue
# Section indices: 0-Lifestyle, 1-Metro, 2-Sports

# Create count variables: count[p][s] = number of photos by photographer p in section s
count = [[Int(f"count_{p}_{s}") for s in range(3)] for p in range(3)]

# Base solver
solver = Solver()

# Non-negativity and integrality: each count is 0, 1, or 2
for p in range(3):
    for s in range(3):
        solver.add(count[p][s] >= 0, count[p][s] <= 2)

# Section totals: each section has exactly 2 photos
for s in range(3):
    solver.add(count[0][s] + count[1][s] + count[2][s] == 2)

# Photographer totals: each photographer has at least 1 and at most 3 photos
for p in range(3):
    solver.add(count[p][0] + count[p][1] + count[p][2] >= 1)
    solver.add(count[p][0] + count[p][1] + count[p][2] <= 3)

# Gagnon cannot be in Sports
solver.add(count[1][2] == 0)

# Lifestyle-Metro overlap constraint: at least one photographer appears in both Lifestyle and Metro
shared = [Bool(f"shared_{p}") for p in range(3)]
for p in range(3):
    solver.add(shared[p] == And(count[p][0] >= 1, count[p][1] >= 1))
solver.add(Or(shared[0], shared[1], shared[2]))

# Hue's Lifestyle count equals Fuentes' Sports count
solver.add(count[2][0] == count[0][2])

# Given condition: Lifestyle has 1 Fuentes and 1 Hue
solver.add(count[0][0] == 1)
solver.add(count[2][0] == 1)

# Answer choices conditions
answer_conditions = [
    count[0][1] == 2,           # A: Both Metro by Fuentes
    count[1][1] == 2,           # B: Both Metro by Gagnon
    count[2][1] == 1,           # C: Exactly one Metro by Hue
    count[2][2] == 2,           # D: Both Sports by Hue
    count[2][2] == 0            # E: Neither Sports by Hue
]

# Check each answer choice
answer_index_list = []
for idx, cond in enumerate(answer_conditions):
    s_chk = Solver()
    # Add all base constraints plus given condition
    for a in solver.assertions():
        s_chk.add(a)
    # Add the specific choice condition
    s_chk.add(cond)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)