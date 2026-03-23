from z3 import *

# Define variables for the six targets: I_w, I_v, S_w, S_v, T_w, T_v
I_w = Int('I_w')
I_v = Int('I_v')
S_w = Int('S_w')
S_v = Int('S_v')
T_w = Int('T_w')
T_v = Int('T_v')

solver = Solver()

# Domain constraints: all targets in {1, 2, 3}
for var in [I_w, I_v, S_w, S_v, T_w, T_v]:
    solver.add(Or(var == 1, var == 2, var == 3))

# Website ≤ voicemail per client
solver.add(I_w <= I_v)
solver.add(S_w <= S_v)
solver.add(T_w <= T_v)

# Image's voicemail is strictly shorter than the other clients' voicemail targets
solver.add(I_v < S_v)
solver.add(I_v < T_v)

# Solide's website target must be shorter than Truvest's website target
solver.add(S_w < T_w)

# Given condition: Image's website target is 2 days
solver.add(I_w == 2)

# Answer choices indices:
# 0: Image's voicemail target
# 1: Solide's website target
# 2: Solide's voicemail target
# 3: Truvest's website target
# 4: Truvest's voicemail target

answer_index_list = []

# Check if Image's voicemail must be 2
s_chk = Solver()
s_chk.add(solver.assertions())
s_chk.add(I_v != 2)
if s_chk.check() == unsat:
    answer_index_list.append(0)

# Check if Solide's website must be 2
s_chk = Solver()
s_chk.add(solver.assertions())
s_chk.add(S_w != 2)
if s_chk.check() == unsat:
    answer_index_list.append(1)

# Check if Solide's voicemail must be 2
s_chk = Solver()
s_chk.add(solver.assertions())
s_chk.add(S_v != 2)
if s_chk.check() == unsat:
    answer_index_list.append(2)

# Check if Truvest's website must be 2
s_chk = Solver()
s_chk.add(solver.assertions())
s_chk.add(T_w != 2)
if s_chk.check() == unsat:
    answer_index_list.append(3)

# Check if Truvest's voicemail must be 2
s_chk = Solver()
s_chk.add(solver.assertions())
s_chk.add(T_v != 2)
if s_chk.check() == unsat:
    answer_index_list.append(4)

print(answer_index_list)