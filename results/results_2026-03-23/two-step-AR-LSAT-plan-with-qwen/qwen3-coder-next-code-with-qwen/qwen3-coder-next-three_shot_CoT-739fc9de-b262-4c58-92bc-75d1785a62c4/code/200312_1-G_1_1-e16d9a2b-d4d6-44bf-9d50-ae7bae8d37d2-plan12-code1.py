from z3 import *

# Scientists: botanists (F=0, G=1, H=2), chemists (K=3, L=4, M=5), zoologists (P=6, Q=7, R=8)
selected = [Bool(f"selected_{i}") for i in range(9)]

solver = Solver()

# Panel size constraint: exactly 5 scientists
solver.add(Sum([If(s, 1, 0) for s in selected]) == 5)

# Type coverage constraints
solver.add(Sum([If(selected[i], 1, 0) for i in range(3)]) >= 1)  # at least one botanist
solver.add(Sum([If(selected[i], 1, 0) for i in range(3, 6)]) >= 1)  # at least one chemist
solver.add(Sum([If(selected[i], 1, 0) for i in range(6, 9)]) >= 1)  # at least one zoologist

# Conditional constraint: if more than one botanist, then at most one zoologist
botanists = Sum([If(selected[i], 1, 0) for i in range(3)])
zoologists = Sum([If(selected[i], 1, 0) for i in range(6, 9)])
solver.add(Implies(botanists >= 2, zoologists <= 1))

# Exclusion constraint: F and K cannot both be selected
solver.add(Not(And(selected[0], selected[3])))

# Exclusion constraint: K and M cannot both be selected
solver.add(Not(And(selected[3], selected[5])))

# Conditional constraint: if M is selected, both P and R must be selected
solver.add(Implies(selected[5], And(selected[6], selected[8])))

# Answer choices
answer_choices = [
    [0, 1, 3, 6, 7],  # F, G, K, P, Q
    [1, 2, 3, 4, 5],  # G, H, K, L, M
    [1, 2, 3, 4, 8],  # G, H, K, L, R
    [2, 3, 5, 6, 8],  # H, K, M, P, R
    [2, 4, 5, 6, 7]   # H, L, M, P, Q
]

# Check each answer choice
answer_index = -1
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert exactly the scientists in the choice are selected
    for i in range(9):
        if i in choice:
            s_chk.add(selected[i] == True)
        else:
            s_chk.add(selected[i] == False)
    
    if s_chk.check() == sat:
        answer_index = idx
        break

print(answer_index)