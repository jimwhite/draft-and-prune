from z3 import *

# Scientists: F, G, H (botanists), K, L, M (chemists), P, Q, R (zoologists)
F, G, H, K, L, M, P, Q, R = Bools(['F', 'G', 'H', 'K', 'L', 'M', 'P', 'Q', 'R'])

# Base solver
solver = Solver()

# Size constraint: exactly 5 scientists selected
solver.add(F + G + H + K + L + M + P + Q + R == 5)

# Representation constraints: at least one of each type
solver.add(Or(F, G, H))  # at least one botanist
solver.add(Or(K, L, M))  # at least one chemist
solver.add(Or(P, Q, R))  # at least one zoologist

# Conditional constraint: if more than one botanist, then at most one zoologist
botanist_count = If(F, 1, 0) + If(G, 1, 0) + If(H, 1, 0)
zoologist_count = If(P, 1, 0) + If(Q, 1, 0) + If(R, 1, 0)
solver.add(Implies(botanist_count >= 2, zoologist_count <= 1))

# Exclusion constraints
solver.add(Not(And(F, K)))  # F and K cannot both be selected
solver.add(Not(And(K, M)))  # K and M cannot both be selected

# Conditional constraint: if M is selected, then both P and R must be selected
solver.add(Implies(M, And(P, R)))

# Answer choices
answer_choices = [
    ['F', 'G', 'K', 'P', 'Q'],
    ['G', 'H', 'K', 'L', 'M'],
    ['G', 'H', 'K', 'L', 'R'],
    ['H', 'K', 'M', 'P', 'R'],
    ['H', 'L', 'M', 'P', 'Q']
]

# Check each answer choice
answer_index_list = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert selected scientists are True and others False
    all_scientists = ['F', 'G', 'H', 'K', 'L', 'M', 'P', 'Q', 'R']
    for scientist in all_scientists:
        if scientist in choice:
            s_chk.add(eval(scientist))
        else:
            s_chk.add(Not(eval(scientist)))
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)