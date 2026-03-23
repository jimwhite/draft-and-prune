from z3 import *

# Section indices: 0-Lifestyle, 1-Metro, 2-Sports
# Photographer indices: 0-Fuentes, 1-Gagnon, 2-Hue

# Variables for counts in each section
L_f, L_g, L_h = Ints('L_f L_g L_h')
M_f, M_g, M_h = Ints('M_f M_g M_h')
S_f, S_g, S_h = Ints('S_f S_g S_h')

solver = Solver()

# Per-section count constraints
solver.add(L_f + L_g + L_h == 2)
solver.add(M_f + M_g + M_h == 2)
solver.add(S_f + S_g + S_h == 2)

# Per-photographer count constraints: at least 1, at most 3
Fuentes_total = L_f + M_f + S_f
Gagnon_total = L_g + M_g + S_g
Hue_total = L_h + M_h + S_h

solver.add(Fuentes_total >= 1, Fuentes_total <= 3)
solver.add(Gagnon_total >= 1, Gagnon_total <= 3)
solver.add(Hue_total >= 1, Hue_total <= 3)

# Gagnon-in-Sports constraint: no Gagnon photos in Sports
solver.add(S_g == 0)

# Cross-section constraint: at least one photo in Lifestyle by photographer who appears in Metro
solver.add(Or(
    And(L_f > 0, M_f > 0),
    And(L_g > 0, M_g > 0),
    And(L_h > 0, M_h > 0)
))

# Fixed premise: Lifestyle has exactly one Fuentes and one Hue (so L_g = 0)
solver.add(L_f == 1, L_h == 1, L_g == 0)

# Matching constraint: Hue in Lifestyle equals Fuentes in Sports
solver.add(L_h == S_f)

# From above: L_h = 1 => S_f = 1
solver.add(S_f == 1)

# From S_f + S_g + S_h = 2 and S_g = 0, S_f = 1 => S_h = 1
solver.add(S_h == 1)

# Answer choices: check each one by adding constraints and testing SAT
answer_index_list = []

# Choice 0: Both photos in Metro are by Fuentes => M_f=2, M_g=0, M_h=0
s_chk = Solver()
s_chk.add(solver.assertions())
s_chk.add(M_f == 2, M_g == 0, M_h == 0)
if s_chk.check() == sat:
    answer_index_list.append(0)

# Choice 1: Both photos in Metro are by Gagnon => M_f=0, M_g=2, M_h=0
s_chk = Solver()
s_chk.add(solver.assertions())
s_chk.add(M_f == 0, M_g == 2, M_h == 0)
if s_chk.check() == sat:
    answer_index_list.append(1)

# Choice 2: Exactly one photograph in Metro section is by Hue => M_h=1
s_chk = Solver()
s_chk.add(solver.assertions())
s_chk.add(M_h == 1)
if s_chk.check() == sat:
    answer_index_list.append(2)

# Choice 3: Both photographs in Sports section are by Hue => S_h=2
s_chk = Solver()
s_chk.add(solver.assertions())
s_chk.add(S_h == 2)
if s_chk.check() == sat:
    answer_index_list.append(3)

# Choice 4: Neither photograph in Sports section is by Hue => S_h=0
s_chk = Solver()
s_chk.add(solver.assertions())
s_chk.add(S_h == 0)
if s_chk.check() == sat:
    answer_index_list.append(4)

print(answer_index_list)