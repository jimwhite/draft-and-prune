from z3 import *

# Photographer indices: 0=Fuentes, 1=Gagnon, 2=Hue
# Section indices: 0=Lifestyle, 1=Metro, 2=Sports

# n[p][s] = number of photos by photographer p in section s
n = [[Int(f"n_{p}_{s}") for s in range(3)] for p in range(3)]

solver = Solver()

# Global photo count: each section has exactly 2 photos
for s in range(3):
    solver.add(n[0][s] + n[1][s] + n[2][s] == 2)

# Photographer global count: each photographer has between 1 and 3 photos
for p in range(3):
    total = Sum([n[p][s] for s in range(3)])
    solver.add(total >= 1, total <= 3)

# Gagnon constraint: no photos in Sports
solver.add(n[1][2] == 0)

# Lifestyle-Metro overlap constraint: at least one photographer has photos in both
overlap = [Bool(f"overlap_{p}") for p in range(3)]
for p in range(3):
    solver.add(overlap[p] == And(n[p][0] > 0, n[p][1] > 0))
solver.add(Or(overlap))

# Hue-Fuentes balance: n[Hue][Lifestyle] = n[Fuentes][Sports]
solver.add(n[2][0] == n[0][2])

# Given condition: Lifestyle has 1 Fuentes and 1 Hue
solver.add(n[0][0] == 1, n[2][0] == 1)
# Since Lifestyle has exactly 2 photos, Gagnon must have 0 in Lifestyle
solver.add(n[1][0] == 0)

# From the balance constraint and given condition: n[2][0] = 1 => n[0][2] = 1
# So Fuentes has exactly 1 photo in Sports

# Since Sports needs 2 photos and Gagnon cannot be in Sports, only Fuentes and Hue can be in Sports
# So n[0][2] + n[2][2] = 2, and we know n[0][2] = 1 => n[2][2] = 1
solver.add(n[0][2] == 1, n[2][2] == 1)

# Now deduce Metro constraints
# For each photographer, compute remaining capacity:
# Fuentes: n[0][0] + n[0][1] + n[0][2] = 1 + n[0][1] + 1 = 2 + n[0][1] <= 3 => n[0][1] <= 1
# Hue: n[2][0] + n[2][1] + n[2][2] = 1 + n[2][1] + 1 = 2 + n[2][1] <= 3 => n[2][1] <= 1
# Gagnon: n[1][0] + n[1][1] + n[1][2] = 0 + n[1][1] + 0 = n[1][1] >= 1 => n[1][1] >= 1

# Metro has exactly 2 photos: n[0][1] + n[1][1] + n[2][1] = 2
solver.add(n[0][1] >= 0, n[0][1] <= 1)
solver.add(n[2][1] >= 0, n[2][1] <= 1)
solver.add(n[1][1] >= 1)
solver.add(n[0][1] + n[1][1] + n[2][1] == 2)

# Answer choices
answer_choices = [
    ("Both Metro photos by Fuentes", lambda: n[0][1] == 2),  # impossible per constraints
    ("Both Metro photos by Gagnon", lambda: n[1][1] == 2),
    ("Exactly one Metro photo by Hue", lambda: n[2][1] == 1),
    ("Both Sports photos by Hue", lambda: n[2][2] == 2),     # contradicts n[2][2] = 1
    ("Neither Sports photo by Hue", lambda: n[2][2] == 0)    # contradicts n[2][2] = 1
]

answer_index_list = []
for idx, (desc, constraint) in enumerate(answer_choices):
    s_chk = Solver()
    # Add all base constraints
    for a in solver.assertions():
        s_chk.add(a)
    
    # Add the specific constraint for this choice
    s_chk.add(constraint())
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)