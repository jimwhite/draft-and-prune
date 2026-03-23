from z3 import *

# Scientists: F, G, H (botanists); K, L, M (chemists); P, Q, R (zoologists)
b_f, b_g, b_h = Bools('b_f b_g b_h')
c_k, c_l, c_m = Bools('c_k c_l c_m')
z_p, z_q, z_r = Bools('z_p z_q z_r')

# Base solver with all constraints
solver = Solver()

# Panel size constraint: exactly 5 scientists
solver.add(b_f + b_g + b_h + c_k + c_l + c_m + z_p + z_q + z_r == 5)

# Type-covering constraint: at least one from each group
solver.add(b_f + b_g + b_h >= 1)
solver.add(c_k + c_l + c_m >= 1)
solver.add(z_p + z_q + z_r >= 1)

# Conditional constraint: if >1 botanist, then ≤1 zoologist
solver.add(Implies(b_f + b_g + b_h >= 2, z_p + z_q + z_r <= 1))

# F and K cannot both be selected
solver.add(Not(And(b_f, c_k)))

# K and M cannot both be selected
solver.add(Not(And(c_k, c_m)))

# If M is selected, both P and R must be selected
solver.add(Implies(c_m, And(z_p, z_r)))

# Answer choices
answer_choices = [
    {'F': 1, 'G': 1, 'H': 0, 'K': 1, 'L': 0, 'M': 0, 'P': 1, 'Q': 1, 'R': 0},  # F, G, K, P, Q
    {'F': 0, 'G': 1, 'H': 1, 'K': 1, 'L': 0, 'M': 1, 'P': 0, 'Q': 0, 'R': 0},  # G, H, K, L, M
    {'F': 0, 'G': 1, 'H': 1, 'K': 1, 'L': 0, 'M': 0, 'P': 0, 'Q': 0, 'R': 1},  # G, H, K, L, R
    {'F': 0, 'G': 0, 'H': 1, 'K': 1, 'L': 0, 'M': 1, 'P': 1, 'Q': 0, 'R': 1},  # H, K, M, P, R
    {'F': 0, 'G': 0, 'H': 1, 'L': 1, 'M': 1, 'P': 1, 'Q': 1, 'R': 0}           # H, L, M, P, Q
]

# Check each answer choice
answer_index_list = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Fix selection to match the choice
    if choice['F'] == 1:
        s_chk.add(b_f)
    else:
        s_chk.add(Not(b_f))
        
    if choice['G'] == 1:
        s_chk.add(b_g)
    else:
        s_chk.add(Not(b_g))
        
    if choice['H'] == 1:
        s_chk.add(b_h)
    else:
        s_chk.add(Not(b_h))
        
    if choice['K'] == 1:
        s_chk.add(c_k)
    else:
        s_chk.add(Not(c_k))
        
    if choice['L'] == 1:
        s_chk.add(c_l)
    else:
        s_chk.add(Not(c_l))
        
    if choice['M'] == 1:
        s_chk.add(c_m)
    else:
        s_chk.add(Not(c_m))
        
    if choice['P'] == 1:
        s_chk.add(z_p)
    else:
        s_chk.add(Not(z_p))
        
    if choice['Q'] == 1:
        s_chk.add(z_q)
    else:
        s_chk.add(Not(z_q))
        
    if choice['R'] == 1:
        s_chk.add(z_r)
    else:
        s_chk.add(Not(z_r))
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)