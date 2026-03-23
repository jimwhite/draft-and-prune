from z3 import *

# Scientists: F, G, H (botanists); K, L, M (chemists); P, Q, R (zoologists)
F, G, H = Bools('F G H')
K, L, M = Bools('K L M')
P, Q, R = Bools('P Q R')

# Base solver
solver = Solver()

# Type count constraints
botanist_count = If(F, 1, 0) + If(G, 1, 0) + If(H, 1, 0)
chemist_count = If(K, 1, 0) + If(L, 1, 0) + If(M, 1, 0)
zoologist_count = If(P, 1, 0) + If(Q, 1, 0) + If(R, 1, 0)

# Panel must include at least one scientist of each type
solver.add(botanist_count >= 1)
solver.add(chemist_count >= 1)
solver.add(zoologist_count >= 1)

# Total panel size is exactly 5
solver.add(botanist_count + chemist_count + zoologist_count == 5)

# If more than one botanist is selected, then at most one zoologist is selected
solver.add(Implies(botanist_count >= 2, zoologist_count <= 1))

# F and K cannot both be selected
solver.add(Not(And(F, K)))

# K and M cannot both be selected
solver.add(Not(And(K, M)))

# If M is selected, both P and R must be selected
solver.add(Implies(M, And(P, R)))

# Answer choices
answer_choices = [
    # 'F, G, K, P, Q'
    [F, G, Not(H), K, Not(L), Not(M), P, Q, Not(R)],
    # 'G, H, K, L, M'
    [Not(F), G, H, K, L, M, Not(P), Not(Q), Not(R)],
    # 'G, H, K, L, R'
    [Not(F), G, H, K, L, Not(M), Not(P), Not(Q), R],
    # 'H, K, M, P, R'
    [Not(F), Not(G), H, K, Not(L), M, P, Not(Q), R],
    # 'H, L, M, P, Q'
    [Not(F), Not(G), H, Not(K), L, M, P, Q, Not(R)]
]

# Check each answer choice
answer_index_list = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert the specific selection assignments for this choice
    s_chk.add(choice)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)