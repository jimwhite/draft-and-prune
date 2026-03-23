from z3 import *

# Photographer indices: 0-Fuentes, 1-Gagnon, 2-Hue
# Section indices: 0-Lifestyle, 1-Metro, 2-Sports

# Create integer variables for counts: p_s[i][j] = count of photographer i in section j
p_s = [[Int(f"p_{i}_{j}") for j in range(3)] for i in range(3)]

# Base solver
solver = Solver()

# Total per section constraints: each section has exactly 2 photos
for j in range(3):
    solver.add(p_s[0][j] + p_s[1][j] + p_s[2][j] == 2)

# Photographer count constraints: each photographer has between 1 and 3 photos
for i in range(3):
    total = p_s[i][0] + p_s[i][1] + p_s[i][2]
    solver.add(total >= 1, total <= 3)

# Gagnon-Sports ban: no Gagnon photos in Sports
solver.add(p_s[1][2] == 0)

# Lifestyle-Metro overlap constraint: at least one photographer has photos in both Lifestyle and Metro
solver.add(Or(
    And(p_s[0][0] > 0, p_s[0][1] > 0),
    And(p_s[1][0] > 0, p_s[1][1] > 0),
    And(p_s[2][0] > 0, p_s[2][1] > 0)
))

# Cross-section equality constraint: h_l == f_s
solver.add(p_s[2][0] == p_s[0][2])

# Given condition: f_l == 1 and h_l == 1
solver.add(p_s[0][0] == 1)
solver.add(p_s[2][0] == 1)

# From the given condition and cross-section equality, we have f_s = 1
solver.add(p_s[0][2] == 1)

# From Lifestyle total: f_l + g_l + h_l = 2 => 1 + g_l + 1 = 2 => g_l = 0
solver.add(p_s[1][0] == 0)

# From Sports total: f_s + g_s + h_s = 2 => 1 + 0 + h_s = 2 => h_s = 1
solver.add(p_s[2][2] == 1)

# From Hue total constraint: 1 <= h_l + h_m + h_s <= 3 => 1 <= 1 + h_m + 1 <= 3 => h_m <= 1
# But from Metro total: f_m + g_m + h_m = 2, and we'll derive more constraints
# From Fuentes total: 1 <= f_l + f_m + f_s <= 3 => 1 <= 1 + f_m + 1 <= 3 => f_m <= 1
solver.add(p_s[0][1] <= 1)

# From Metro total: f_m + g_m + h_m = 2
solver.add(p_s[0][1] + p_s[1][1] + p_s[2][1] == 2)

# From Hue total: h_m + h_s <= 1 (since h_l=1, and total <=3) => h_m + 1 <= 1 => h_m = 0
solver.add(p_s[2][1] == 0)

# With h_m = 0, Metro total becomes: f_m + g_m = 2
# And from earlier: f_m <= 1, so g_m >= 1

# Check each answer choice
answer_choices = [
    "Both Metro by Fuentes",      # index 0: f_m == 2
    "Both Metro by Gagnon",       # index 1: g_m == 2, f_m == 0
    "Exactly one Metro by Hue",   # index 2: h_m == 1
    "Both Sports by Hue",         # index 3: h_s == 2
    "Neither Sports by Hue"       # index 4: h_s == 0
]

answer_index_list = []

# Check choice 0: Both Metro by Fuentes (f_m == 2)
s_chk = Solver()
s_chk.add(solver.assertions())
s_chk.add(p_s[0][1] == 2)
if s_chk.check() == unsat:
    answer_index_list.append(0)

# Check choice 1: Both Metro by Gagnon (g_m == 2, f_m == 0)
s_chk = Solver()
s_chk.add(solver.assertions())
s_chk.add(p_s[1][1] == 2)
s_chk.add(p_s[0][1] == 0)
if s_chk.check() == sat:
    answer_index_list.append(1)

# Check choice 2: Exactly one Metro by Hue (h_m == 1)
s_chk = Solver()
s_chk.add(solver.assertions())
s_chk.add(p_s[2][1] == 1)
if s_chk.check() == unsat:
    answer_index_list.append(2)

# Check choice 3: Both Sports by Hue (h_s == 2)
s_chk = Solver()
s_chk.add(solver.assertions())
s_chk.add(p_s[2][2] == 2)
if s_chk.check() == unsat:
    answer_index_list.append(3)

# Check choice 4: Neither Sports by Hue (h_s == 0)
s_chk = Solver()
s_chk.add(solver.assertions())
s_chk.add(p_s[2][2] == 0)
if s_chk.check() == unsat:
    answer_index_list.append(4)

print(answer_index_list)