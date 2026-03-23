from z3 import *

# Photographer indices: 0-Fuentes, 1-Gagnon, 2-Hue
# Section indices: 0-Lifestyle, 1-Metro, 2-Sports

# Create integer variables for counts: count[p][s] = number of photos by photographer p in section s
count = [[Int(f"count_{p}_{s}") for s in range(3)] for p in range(3)]

solver = Solver()

# Total count constraints: each photographer has 1-3 photos total
for p in range(3):
    solver.add(Sum(count[p]) >= 1, Sum(count[p]) <= 3)

# Section size constraints: each section has exactly 2 photos
for s in range(3):
    solver.add(Sum([count[p][s] for p in range(3)]) == 2)

# Gagnon constraint: no Gagnon photos in Sports
solver.add(count[1][2] == 0)

# Lifestyle/Metro overlap constraint: at least one photographer has photos in both Lifestyle and Metro
overlap_constraint = Or(
    And(count[0][0] >= 1, count[0][1] >= 1),
    And(count[1][0] >= 1, count[1][1] >= 1),
    And(count[2][0] >= 1, count[2][1] >= 1)
)
solver.add(overlap_constraint)

# Hue/Fuentes balance constraint: Hue in Lifestyle = Fuentes in Sports
solver.add(count[2][0] == count[0][2])

# Given condition: Lifestyle has exactly one Fuentes and one Hue
solver.add(count[0][0] == 1, count[2][0] == 1)

# Since Lifestyle total is 2 and we have Fuentes=1, Hue=1, Gagnon must be 0 in Lifestyle
solver.add(count[1][0] == 0)

# From Hue/Fuentes balance: count[2][0]=1 => count[0][2]=1 (Fuentes in Sports = 1)
solver.add(count[0][2] == 1)

# From Sports total: count[0][2] + count[1][2] + count[2][2] = 2, and count[1][2]=0
# So: 1 + 0 + count[2][2] = 2 => count[2][2] = 1
solver.add(count[2][2] == 1)

# Gagnon total constraint: count[1][0]=0, count[1][2]=0 => Gagnon total = count[1][1]
# Must be >= 1 and <= 3
solver.add(count[1][1] >= 1, count[1][1] <= 3)

# Fuentes total: count[0][0]=1, count[0][2]=1 => total = 2 + count[0][1]
# Must be <= 3 => count[0][1] <= 1
solver.add(count[0][1] <= 1)

# Metro total constraint: count[0][1] + count[1][1] + count[2][1] = 2
solver.add(count[0][1] + count[1][1] + count[2][1] == 2)

# Hue total: count[2][0]=1, count[2][2]=1 => total = 2 + count[2][1]
# Must be <= 3 => count[2][1] <= 1
solver.add(count[2][1] <= 1)

# Answer choices (0-indexed):
# A: Both Metro by Fuentes => count[0][1]=2, count[1][1]=0, count[2][1]=0
# B: Both Metro by Gagnon => count[1][1]=2, count[0][1]=0, count[2][1]=0
# C: Exactly one Metro by Hue => count[2][1]=1, then from constraints: count[0][1]=0, count[1][1]=1
# D: Both Sports by Hue => contradicts count[0][2]=1
# E: Neither Sports by Hue => count[2][2]=0, contradicts our earlier deduction

# We'll check each choice by adding the specific constraints and checking SAT
answer_index_list = []

# Choice A: Both Metro by Fuentes
s_chk = Solver()
s_chk.add(solver.assertions())
s_chk.add(count[0][1] == 2, count[1][1] == 0, count[2][1] == 0)
if s_chk.check() == unsat:
    answer_index_list.append(0)

# Choice B: Both Metro by Gagnon
s_chk = Solver()
s_chk.add(solver.assertions())
s_chk.add(count[0][1] == 0, count[1][1] == 2, count[2][1] == 0)
if s_chk.check() == unsat:
    answer_index_list.append(1)

# Choice C: Exactly one Metro by Hue
s_chk = Solver()
s_chk.add(solver.assertions())
s_chk.add(count[2][1] == 1)
# From Metro total: count[0][1] + count[1][1] = 1
# From Gagnon constraint: count[1][1] >= 1 => count[1][1]=1, count[0][1]=0
s_chk.add(count[0][1] == 0, count[1][1] == 1)
if s_chk.check() == sat:
    answer_index_list.append(2)

# Choice D: Both Sports by Hue
s_chk = Solver()
s_chk.add(solver.assertions())
s_chk.add(count[2][2] == 2)
if s_chk.check() == unsat:
    answer_index_list.append(3)

# Choice E: Neither Sports by Hue
s_chk = Solver()
s_chk.add(solver.assertions())
s_chk.add(count[2][2] == 0)
if s_chk.check() == unsat:
    answer_index_list.append(4)

print(answer_index_list)