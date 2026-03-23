from z3 import *

# Scientists: F, G, H (botanists); K, L, M (chemists); P, Q, R (zoologists)
scientists = ["F", "G", "H", "K", "L", "M", "P", "Q", "R"]
sel = {s: Bool(f"sel_{s}") for s in scientists}

solver = Solver()

# Exactly five scientists
solver.add(Sum([If(sel[s], 1, 0) for s in scientists]) == 5)

# At least one from each category
botanists = ["F", "G", "H"]
chemists = ["K", "L", "M"]
zoologists = ["P", "Q", "R"]

solver.add(Sum([If(sel[s], 1, 0) for s in botanists]) >= 1)
solver.add(Sum([If(sel[s], 1, 0) for s in chemists]) >= 1)
solver.add(Sum([If(sel[s], 1, 0) for s in zoologists]) >= 1)

# If more than one botanist, then at most one zoologist
bot_count = Sum([If(sel[s], 1, 0) for s in botanists])
zoo_count = Sum([If(sel[s], 1, 0) for s in zoologists])
solver.add(Implies(bot_count >= 2, zoo_count <= 1))

# F and K cannot both be selected
solver.add(Not(And(sel["F"], sel["K"])))

# K and M cannot both be selected
solver.add(Not(And(sel["K"], sel["M"])))

# If M is selected, both P and R must be selected
solver.add(Implies(sel["M"], And(sel["P"], sel["R"])))

# Answer choices
choices = [
    ['F', 'G', 'K', 'P', 'Q'],
    ['G', 'H', 'K', 'L', 'M'],
    ['G', 'H', 'K', 'L', 'R'],
    ['H', 'K', 'M', 'P', 'R'],
    ['H', 'L', 'M', 'P', 'Q']
]

# Check each choice
answer_index_list = []
for idx, choice in enumerate(choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert exactly the scientists in this choice are selected
    for s in scientists:
        if s in choice:
            s_chk.add(sel[s])
        else:
            s_chk.add(Not(sel[s]))
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

# Output the first acceptable choice (as per question format)
if answer_index_list:
    print(choices[answer_index_list[0]])
else:
    print([])