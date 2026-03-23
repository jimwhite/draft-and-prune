from z3 import *

# Photographer indices: F=0, G=1, H=2
# Section indices: L=0, M=1, S=2

# Create count variables: count[p][s] = number of photos by photographer p in section s
count = [[Int(f"count_{p}_{s}") for s in range(3)] for p in range(3)]

solver = Solver()

# Global constraints
# Each section has exactly 2 photos
for s in range(3):
    solver.add(count[0][s] + count[1][s] + count[2][s] == 2)

# Each photographer has between 1 and 3 photos total
for p in range(3):
    solver.add(Sum([count[p][s] for s in range(3)]) >= 1)
    solver.add(Sum([count[p][s] for s in range(3)]) <= 3)

# Gagnon not in Sports
solver.add(count[1][2] == 0)

# Given: Lifestyle has exactly one Fuentes and one Hue
solver.add(count[0][0] == 1)  # Fuentes in Lifestyle
solver.add(count[2][0] == 1)  # Hue in Lifestyle
# Therefore Gagnon in Lifestyle = 0 (since total per section is 2)
solver.add(count[1][0] == 0)

# Metro-Security constraint: At least one photographer in Lifestyle also appears in Metro
# Since Lifestyle has Fuentes (p=0) and Hue (p=2), we need:
# (count[0][1] > 0) OR (count[2][1] > 0)
solver.add(Or(count[0][1] > 0, count[2][1] > 0))

# Hue-Lifestyle = Fuentes-Sports constraint
solver.add(count[2][0] == count[0][2])  # Since count[2][0] = 1, this forces count[0][2] = 1

# From Sports section: count[0][2] + count[1][2] + count[2][2] = 2
# With count[0][2] = 1 and count[1][2] = 0, we get count[2][2] = 1
solver.add(count[2][2] == 1)

# Answer choices (0-indexed)
answer_choices = [
    "Both Metro Fuentes",      # count[0][1] == 2
    "Both Metro Gagnon",       # count[1][1] == 2
    "Exactly one Metro Hue",   # count[2][1] == 1
    "Both Sports Hue",         # count[2][2] == 2
    "Neither Sports Hue"       # count[2][2] == 0
]

answer_index_list = []

for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    # Add all base constraints
    for a in solver.assertions():
        s_chk.add(a)
    
    # Add choice-specific constraint
    if idx == 0:  # Both Metro Fuentes
        s_chk.add(count[0][1] == 2)
    elif idx == 1:  # Both Metro Gagnon
        s_chk.add(count[1][1] == 2)
    elif idx == 2:  # Exactly one Metro Hue
        s_chk.add(count[2][1] == 1)
    elif idx == 3:  # Both Sports Hue
        s_chk.add(count[2][2] == 2)
    elif idx == 4:  # Neither Sports Hue
        s_chk.add(count[2][2] == 0)
    
    # Check satisfiability
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)