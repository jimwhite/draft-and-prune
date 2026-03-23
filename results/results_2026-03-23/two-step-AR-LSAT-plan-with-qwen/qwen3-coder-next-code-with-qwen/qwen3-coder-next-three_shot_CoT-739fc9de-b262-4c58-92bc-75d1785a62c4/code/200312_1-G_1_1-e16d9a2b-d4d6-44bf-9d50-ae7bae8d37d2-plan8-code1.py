from z3 import *

# Scientists: 0-F, 1-G, 2-H (botanists)
#            3-K, 4-L, 5-M (chemists)
#            6-P, 7-Q, 8-R (zoologists)

s = [Bool(f"s_{i}") for i in range(9)]

solver = Solver()

# Exactly five scientists selected
solver.add(Sum([If(x, 1, 0) for x in s]) == 5)

# At least one of each type
solver.add(Or(s[0], s[1], s[2]))  # botanist
solver.add(Or(s[3], s[4], s[5]))  # chemist
solver.add(Or(s[6], s[7], s[8]))  # zoologist

# If more than one botanist, then at most one zoologist
bot_count = Sum([If(s[i], 1, 0) for i in range(3)])
zoo_count = Sum([If(s[i], 1, 0) for i in range(6, 9)])
solver.add(Or(bot_count <= 1, zoo_count <= 1))

# F and K cannot both be selected
solver.add(Not(And(s[0], s[3])))

# K and M cannot both be selected
solver.add(Not(And(s[3], s[5])))

# If M is selected, both P and R must be selected
solver.add(Implies(s[5], And(s[6], s[8])))

# Answer choices
choices = [
    [0, 1, 3, 6, 7],   # F, G, K, P, Q
    [1, 2, 3, 4, 5],   # G, H, K, L, M
    [1, 2, 3, 4, 8],   # G, H, K, L, R
    [2, 3, 5, 6, 8],   # H, K, M, P, R
    [2, 4, 5, 6, 7]    # H, L, M, P, Q
]

acceptable_indices = []

for idx, choice in enumerate(choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert the specific choice
    for i in range(9):
        if i in choice:
            s_chk.add(s[i])
        else:
            s_chk.add(Not(s[i]))
    
    if s_chk.check() == sat:
        acceptable_indices.append(idx)

# Print the first acceptable choice index (as per question format)
print(acceptable_indices[0] if acceptable_indices else -1)