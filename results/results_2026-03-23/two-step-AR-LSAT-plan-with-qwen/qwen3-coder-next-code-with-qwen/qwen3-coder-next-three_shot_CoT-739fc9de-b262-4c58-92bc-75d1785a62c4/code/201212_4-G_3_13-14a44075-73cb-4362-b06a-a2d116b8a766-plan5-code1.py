from z3 import *

# Target variables: I_w, I_v, S_w, S_v, T_w, T_v
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

# Image's voicemail target must be shorter than both others' voicemail targets
solver.add(I_v < S_v)
solver.add(I_v < T_v)

# Solide's website target must be shorter than Truvest's website target
solver.add(S_w < T_w)

# Given condition: Image's website target is 2 days
solver.add(I_w == 2)

# Check each choice for necessity (must be 2)
answer_choices = [
    I_v,   # Image's voicemail target
    S_w,   # Solide's website target
    S_v,   # Solide's voicemail target
    T_w,   # Truvest's website target
    T_v    # Truvest's voicemail target
]

answer_index_list = []
for idx, var in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert this variable is NOT 2
    s_chk.add(var != 2)
    
    # If UNSAT, then this variable must be 2
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)