from z3 import *

# Scientist indices: F=0, G=1, H=2 (botanists); K=3, L=4, M=5 (chemists); P=6, Q=7, R=8 (zoologists)
s = [Bool(f"s_{i}") for i in range(9)]

# Base solver
solver = Solver()

# Panel size constraint: exactly 5 scientists selected
solver.add(Sum([If(s[i], 1, 0) for i in range(9)]) == 5)

# Representation constraints: at least one of each type
solver.add(Sum([If(s[i], 1, 0) for i in range(3)]) >= 1)  # botanists
solver.add(Sum([If(s[i], 1, 0) for i in range(3, 6)]) >= 1)  # chemists
solver.add(Sum([If(s[i], 1, 0) for i in range(6, 9)]) >= 1)  # zoologists

# Conditional constraints
# If more than one botanist, then at most one zoologist
botanists = Sum([If(s[i], 1, 0) for i in range(3)])
zoologists = Sum([If(s[i], 1, 0) for i in range(6, 9)])
solver.add(Implies(botanists > 1, zoologists <= 1))

# F and K cannot both be selected
solver.add(Not(And(s[0], s[3])))

# K and M cannot both be selected
solver.add(Not(And(s[3], s[5])))

# If M is selected, both P and R must be selected
solver.add(Implies(s[5], And(s[6], s[8])))

# Answer choices
answer_choices = [
    [0, 1, 3, 6, 7],   # F, G, K, P, Q
    [1, 2, 3, 4, 5],   # G, H, K, L, M
    [1, 2, 3, 4, 8],   # G, H, K, L, R
    [2, 3, 5, 6, 8],   # H, K, M, P, R
    [2, 4, 5, 6, 7]    # H, L, M, P, Q
]

# Check each answer choice
answer_index_list = []
for idx, selected in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert specific selections
    for i in range(9):
        if i in selected:
            s_chk.add(s[i])
        else:
            s_chk.add(Not(s[i]))
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)