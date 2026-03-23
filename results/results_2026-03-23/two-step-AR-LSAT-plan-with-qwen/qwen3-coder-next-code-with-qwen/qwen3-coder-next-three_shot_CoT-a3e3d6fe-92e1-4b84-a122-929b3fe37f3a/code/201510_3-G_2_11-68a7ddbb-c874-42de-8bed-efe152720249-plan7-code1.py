from z3 import *

# Photographer indices: 0=Fuentes, 1=Gagnon, 2=Hue
# Section indices: 0=Lifestyle, 1=Metro, 2=Sports

# count[p][s] = number of photographer p's photos in section s
count = [[Int(f"count_{p}_{s}") for s in range(3)] for p in range(3)]

# Base solver
solver = Solver()

# Section size constraints: each section has exactly 2 photos
for s in range(3):
    solver.add(count[0][s] + count[1][s] + count[2][s] == 2)

# Per-photographer global count constraints: each photographer has 1-3 photos
for p in range(3):
    total = Sum([count[p][s] for s in range(3)])
    solver.add(total >= 1, total <= 3)

# Gagnon constraint: no photos in Sports
solver.add(count[1][2] == 0)

# Given condition: Lifestyle has 1 Fuentes and 1 Hue
solver.add(count[0][0] == 1)
solver.add(count[2][0] == 1)

# Hue-Lifestyle/Fuentes-Sports equality constraint
solver.add(count[2][0] == count[0][2])

# Lifestyle-Metro overlap constraint: at least one photographer appears in both
shared = [Bool(f"shared_{p}") for p in range(3)]
for p in range(3):
    solver.add(shared[p] == And(count[p][0] > 0, count[p][1] > 0))
solver.add(Or(shared))

# Non-negativity and upper bound constraints for counts
for p in range(3):
    for s in range(3):
        solver.add(count[p][s] >= 0, count[p][s] <= 2)

# Answer choices
answer_choices = [
    "Both Metro by Fuentes",      # 0: count[0][1] == 2
    "Both Metro by Gagnon",       # 1: count[1][1] == 2
    "Exactly one Metro by Hue",   # 2: count[2][1] == 1
    "Both Sports by Hue",         # 3: count[2][2] == 2
    "Neither Sports by Hue"       # 4: count[2][2] == 0
]

# Check each answer choice
answer_index_list = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add specific constraint for the choice
    if idx == 0:  # Both Metro by Fuentes
        s_chk.add(count[0][1] == 2)
    elif idx == 1:  # Both Metro by Gagnon
        s_chk.add(count[1][1] == 2)
    elif idx == 2:  # Exactly one Metro by Hue
        s_chk.add(count[2][1] == 1)
    elif idx == 3:  # Both Sports by Hue
        s_chk.add(count[2][2] == 2)
    elif idx == 4:  # Neither Sports by Hue
        s_chk.add(count[2][2] == 0)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)