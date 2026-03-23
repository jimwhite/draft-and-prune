from z3 import *

# Scientists: F, G, H (botanists), K, L, M (chemists), P, Q, R (zoologists)
scientists = ["F", "G", "H", "K", "L", "M", "P", "Q", "R"]
selected = [Bool(f"sel_{s}") for s in scientists]

# Group membership
botanists = [0, 1, 2]   # F, G, H
chemists = [3, 4, 5]    # K, L, M
zoologists = [6, 7, 8]  # P, Q, R

# Base solver
solver = Solver()

# Exactly 5 scientists selected
solver.add(Sum([If(selected[i], 1, 0) for i in range(9)]) == 5)

# At least one of each type
solver.add(Or(selected[botanists[0]], selected[botanists[1]], selected[botanists[2]]))
solver.add(Or(selected[chemists[0]], selected[chemists[1]], selected[chemists[2]]))
solver.add(Or(selected[zoologists[0]], selected[zoologists[1]], selected[zoologists[2]]))

# If more than one botanist, then at most one zoologist
bot_count = Sum([If(selected[i], 1, 0) for i in botanists])
zoo_count = Sum([If(selected[i], 1, 0) for i in zoologists])
solver.add(Implies(bot_count >= 2, zoo_count <= 1))

# F and K cannot both be selected
solver.add(Not(And(selected[0], selected[3])))

# K and M cannot both be selected
solver.add(Not(And(selected[3], selected[5])))

# If M is selected, both P and R must be selected
solver.add(Implies(selected[5], And(selected[6], selected[8])))

# Answer choices
answer_choices = [
    ["F", "G", "K", "P", "Q"],  # Choice 0
    ["G", "H", "K", "L", "M"],  # Choice 1
    ["G", "H", "K", "L", "R"],  # Choice 2
    ["H", "K", "M", "P", "R"],  # Choice 3
    ["H", "L", "M", "P", "Q"]   # Choice 4
]

# Check each choice
answer_index_list = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Force exactly the scientists in this choice to be selected
    for i, s in enumerate(scientists):
        if s in choice:
            s_chk.add(selected[i])
        else:
            s_chk.add(Not(selected[i]))
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

# Output the first SAT choice index (as per question format)
print(answer_index_list[0] if answer_index_list else -1)