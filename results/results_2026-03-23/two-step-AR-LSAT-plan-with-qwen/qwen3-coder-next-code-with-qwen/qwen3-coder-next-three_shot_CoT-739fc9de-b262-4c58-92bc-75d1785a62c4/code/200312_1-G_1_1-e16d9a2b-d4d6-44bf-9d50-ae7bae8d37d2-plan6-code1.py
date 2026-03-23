from z3 import *

# Scientists: F, G, H (botanists), K, L, M (chemists), P, Q, R (zoologists)
scientists = ["F", "G", "H", "K", "L", "M", "P", "Q", "R"]
# Map scientists to indices
indices = {s: i for i, s in enumerate(scientists)}

# Selection variables
sel = [Bool(f"sel_{s}") for s in scientists]

# Base solver
solver = Solver()

# Field mapping
botanists = [indices["F"], indices["G"], indices["H"]]
chemists = [indices["K"], indices["L"], indices["M"]]
zoologists = [indices["P"], indices["Q"], indices["R"]]

# Field coverage constraint: at least one of each type
solver.add(Or(sel[botanists[0]], sel[botanists[1]], sel[botanists[2]]))
solver.add(Or(sel[chemists[0]], sel[chemists[1]], sel[chemists[2]]))
solver.add(Or(sel[zoologists[0]], sel[zoologists[1]], sel[zoologists[2]]))

# Size constraint: exactly 5 scientists
solver.add(Sum([If(s, 1, 0) for s in sel]) == 5)

# If more than one botanist, then at most one zoologist
count_botanists = Sum([If(sel[i], 1, 0) for i in botanists])
count_zoologists = Sum([If(sel[i], 1, 0) for i in zoologists])
solver.add(Implies(count_botanists >= 2, count_zoologists <= 1))

# F and K cannot both be selected
solver.add(Not(And(sel[indices["F"]], sel[indices["K"]])))

# K and M cannot both be selected
solver.add(Not(And(sel[indices["K"]], sel[indices["M"]])))

# If M is selected, both P and R must be selected
solver.add(Implies(sel[indices["M"]], And(sel[indices["P"]], sel[indices["R"]])))

# Answer choices
answer_choices = [
    ["F", "G", "K", "P", "Q"],
    ["G", "H", "K", "L", "M"],
    ["G", "H", "K", "L", "R"],
    ["H", "K", "M", "P", "R"],
    ["H", "L", "M", "P", "Q"]
]

# Check each answer choice
acceptable_index = -1
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Fix selection for this choice
    selected_set = set(choice)
    for s in scientists:
        if s in selected_set:
            s_chk.add(sel[indices[s]])
        else:
            s_chk.add(Not(sel[indices[s]]))
    
    if s_chk.check() == sat:
        acceptable_index = idx
        break

print(acceptable_index)