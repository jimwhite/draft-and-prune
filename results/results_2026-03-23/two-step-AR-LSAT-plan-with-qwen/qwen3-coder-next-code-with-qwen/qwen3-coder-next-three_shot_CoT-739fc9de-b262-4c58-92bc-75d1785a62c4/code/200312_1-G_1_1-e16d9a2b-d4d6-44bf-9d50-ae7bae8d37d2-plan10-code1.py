from z3 import *

# Scientists: Botanists (F, G, H), Chemists (K, L, M), Zoologists (P, Q, R)
F, G, H = Bools('F G H')
K, L, M = Bools('K L M')
P, Q, R = Bools('P Q R')

# Helper expressions for counts
bot_count = If(F, 1, 0) + If(G, 1, 0) + If(H, 1, 0)
chem_count = If(K, 1, 0) + If(L, 1, 0) + If(M, 1, 0)
zoo_count = If(P, 1, 0) + If(Q, 1, 0) + If(R, 1, 0)

# Base solver
solver = Solver()

# Panel size constraint
solver.add(bot_count + chem_count + zoo_count == 5)

# Must have at least one of each type
solver.add(bot_count >= 1, chem_count >= 1, zoo_count >= 1)

# If more than one botanist, then at most one zoologist
solver.add(Or(bot_count <= 1, zoo_count <= 1))

# F and K cannot both be selected
solver.add(Not(And(F, K)))

# K and M cannot both be selected
solver.add(Not(And(K, M)))

# If M is selected, both P and R must be selected
solver.add(Implies(M, And(P, R)))

# Answer choices
answer_choices = [
    # 'F, G, K, P, Q'
    And(F, G, Not(H), K, Not(L), Not(M), P, Q, Not(R)),
    # 'G, H, K, L, M'
    And(Not(F), G, H, K, L, M, Not(P), Not(Q), Not(R)),
    # 'G, H, K, L, R'
    And(Not(F), G, H, K, L, Not(M), Not(P), Not(Q), R),
    # 'H, K, M, P, R'
    And(Not(F), Not(G), H, K, Not(L), M, P, Not(Q), R),
    # 'H, L, M, P, Q'
    And(Not(F), Not(G), H, Not(K), L, M, P, Q, Not(R))
]

# Check each answer choice
answer_index_list = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(choice)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)