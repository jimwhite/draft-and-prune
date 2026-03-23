from z3 import *

# Photographer indices: 0-Fuentes, 1-Gagnon, 2-Hue
# Section indices: 0-Lifestyle, 1-Metro, 2-Sports

# Variables: f_L, f_M, f_S for Fuentes in each section
f_L, f_M, f_S = Ints('f_L f_M f_S')
# Variables: g_L, g_M, g_S for Gagnon in each section
g_L, g_M, g_S = Ints('g_L g_M g_S')
# Variables: h_L, h_M, h_S for Hue in each section
h_L, h_M, h_S = Ints('h_L h_M h_S')

solver = Solver()

# Per-section constraints: exactly 2 photos per section
solver.add(f_L + g_L + h_L == 2)  # Lifestyle
solver.add(f_M + g_M + h_M == 2)  # Metro
solver.add(f_S + g_S + h_S == 2)  # Sports

# Per-photographer global constraints: at least 1, at most 3
solver.add(1 <= f_L + f_M + f_S, f_L + f_M + f_S <= 3)  # Fuentes
solver.add(1 <= g_L + g_M + g_S, g_L + g_M + g_S <= 3)  # Gagnon
solver.add(1 <= h_L + h_M + h_S, h_L + h_M + h_S <= 3)  # Hue

# Gagnon constraint: no Gagnon in Sports
solver.add(g_S == 0)

# Lifestyle-Metro overlap constraint: at least one photographer appears in both
solver.add(Or(
    And(f_L > 0, f_M > 0),
    And(g_L > 0, g_M > 0),
    And(h_L > 0, h_M > 0)
))

# Hue-Fuentes balance constraint: h_L == f_S
solver.add(h_L == f_S)

# Given condition: Lifestyle has one Fuentes and one Hue
solver.add(f_L == 1, h_L == 1)

# From the given condition and Lifestyle constraint: g_L = 0
solver.add(g_L == 0)

# From h_L == f_S and h_L == 1: f_S = 1
solver.add(f_S == 1)

# From Sports constraint and f_S=1, g_S=0: h_S = 1
solver.add(h_S == 1)

# Answer choices (as additional constraints to check)
answer_choices = [
    f_M == 2,                    # A. Both Metro photos by Fuentes
    And(g_M == 2, f_M == 0, h_M == 0),  # B. Both Metro photos by Gagnon
    h_M == 1,                    # C. Exactly one Metro photo by Hue
    h_S == 2,                    # D. Both Sports photos by Hue (already known h_S=1)
    h_S == 0                     # E. Neither Sports photo by Hue (already known h_S=1)
]

answer_index_list = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    # Add all base constraints plus the given condition deductions
    for assertion in solver.assertions():
        s_chk.add(assertion)
    # Add the specific choice constraint
    s_chk.add(choice)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)