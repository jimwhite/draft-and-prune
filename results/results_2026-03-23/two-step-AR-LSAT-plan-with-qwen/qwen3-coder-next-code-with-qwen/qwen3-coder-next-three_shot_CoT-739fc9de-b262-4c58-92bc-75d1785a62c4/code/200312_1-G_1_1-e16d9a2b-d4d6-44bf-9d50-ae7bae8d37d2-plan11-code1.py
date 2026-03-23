from z3 import *

# Scientist indices: botanists (F,G,H) = 0,1,2; chemists (K,L,M) = 3,4,5; zoologists (P,Q,R) = 6,7,8
s = [Bool(f"s_{i}") for i in range(9)]

# Base solver
solver = Solver()

# Panel size constraint: exactly 5 scientists selected
solver.add(Sum([If(s[i], 1, 0) for i in range(9)]) == 5)

# At-least-one-per-type constraints
solver.add(Sum([If(s[i], 1, 0) for i in range(3)]) >= 1)  # botanists
solver.add(Sum([If(s[i], 1, 0) for i in range(3, 6)]) >= 1)  # chemists
solver.add(Sum([If(s[i], 1, 0) for i in range(6, 9)]) >= 1)  # zoologists

# If more than one botanist, then at most one zoologist
bot_count = Sum([If(s[i], 1, 0) for i in range(3)])
zoo_count = Sum([If(s[i], 1, 0) for i in range(6, 9)])
solver.add(Not(And(bot_count > 1, zoo_count >= 2)))

# F and K incompatible: s[0] + s[3] <= 1
solver.add(s[0] == False or s[3] == False)

# K and M incompatible: s[3] + s[5] <= 1
solver.add(s[3] == False or s[5] == False)

# If M selected, then P and R must be selected
solver.add(Implies(s[5], s[6]))
solver.add(Implies(s[5], s[8]))

# Candidate selections
choices = [
    [0, 1, 3, 6, 7],  # F, G, K, P, Q
    [1, 2, 3, 4, 5],  # G, H, K, L, M
    [1, 2, 3, 4, 8],  # G, H, K, L, R
    [2, 3, 5, 6, 8],  # H, K, M, P, R
    [2, 4, 5, 6, 7]   # H, L, M, P, Q
]

# Check each choice
answer_index = -1
for idx, choice in enumerate(choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert exactly the scientists in the choice are selected
    for i in range(9):
        if i in choice:
            s_chk.add(s[i] == True)
        else:
            s_chk.add(s[i] == False)
    
    if s_chk.check() == sat:
        answer_index = idx
        break

print(answer_index)