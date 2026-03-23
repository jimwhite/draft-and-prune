from z3 import *

# Photographer indices: 0-Fuentes, 1-Gagnon, 2-Hue
# Section indices: 0-Lifestyle, 1-Metro, 2-Sports

# Variables for number of photos per photographer per section
L_f, L_g, L_h = Ints('L_f L_g L_h')
M_f, M_g, M_h = Ints('M_f M_g M_h')
S_f, S_g, S_h = Ints('S_f S_g S_h')

solver = Solver()

# Each section has exactly 2 photos
solver.add(L_f + L_g + L_h == 2)
solver.add(M_f + M_g + M_h == 2)
solver.add(S_f + S_g + S_h == 2)

# Global photo count constraints: each photographer has between 1 and 3 photos
total_f = L_f + M_f + S_f
total_g = L_g + M_g + S_g
total_h = L_h + M_h + S_h

solver.add(total_f >= 1, total_f <= 3)
solver.add(total_g >= 1, total_g <= 3)
solver.add(total_h >= 1, total_h <= 3)

# Lifestyle-Metro cross-section constraint: at least one photographer appears in both
# (L_f > 0 ∧ M_f > 0) ∨ (L_g > 0 ∧ M_g > 0) ∨ (L_h > 0 ∧ M_h > 0)
lf_mf = And(L_f > 0, M_f > 0)
lg_mg = And(L_g > 0, M_g > 0)
lh_mh = And(L_h > 0, M_h > 0)
solver.add(Or(lf_mf, lg_mg, lh_mh))

# Hue-Fuentes balance constraint: L_h == S_f
solver.add(L_h == S_f)

# Gagnon-Sports ban: no Gagnon photos in Sports
solver.add(S_g == 0)

# Given condition: Lifestyle = [Fuentes, Hue] → L_f == 1, L_h == 1, L_g == 0
solver.add(L_f == 1)
solver.add(L_h == 1)
solver.add(L_g == 0)

# Answer choices
answer_choices = [
    ("Both Metro by Fuentes", M_f == 2),
    ("Both Metro by Gagnon", M_g == 2),
    ("Exactly one Metro by Hue", M_h == 1),
    ("Both Sports by Hue", S_h == 2),
    ("Neither Sports by Hue", S_h == 0)
]

# Check each choice
answer_index_list = []
for idx, (desc, constraint) in enumerate(answer_choices):
    s_chk = Solver()
    # Add all base constraints
    for a in solver.assertions():
        s_chk.add(a)
    # Add the specific choice constraint
    s_chk.add(constraint)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)