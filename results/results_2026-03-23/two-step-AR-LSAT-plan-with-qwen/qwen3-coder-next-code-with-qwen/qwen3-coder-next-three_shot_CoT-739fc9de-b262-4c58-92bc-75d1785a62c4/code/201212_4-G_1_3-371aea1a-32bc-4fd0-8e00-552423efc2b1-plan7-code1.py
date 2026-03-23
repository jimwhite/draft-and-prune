from z3 import *

# House indices: J, K, L, M, N, O, P
houses = ["J", "K", "L", "M", "N", "O", "P"]
pos = {h: Int(f"pos_{h}") for h in houses}

# Base solver
solver = Solver()

# Domain constraints: positions 1-7, all distinct
for h in houses:
    solver.add(pos[h] >= 1, pos[h] <= 7)
solver.add(Distinct(*[pos[h] for h in houses]))

# Time slot constraints
def morning(p): return Or(p == 1, p == 2)
def afternoon(p): return Or(p == 3, p == 4, p == 5)
def evening(p): return Or(p == 6, p == 7)

# J must be shown in the evening
solver.add(evening(pos["J"]))

# K cannot be shown in the morning (so afternoon or evening)
solver.add(Not(morning(pos["K"])))

# L after K and before M
solver.add(pos["K"] < pos["L"])
solver.add(pos["L"] < pos["M"])

# Answer choices (indices correspond to the given list)
answer_choices = [
    "K_evening",      # 0: K is shown in the evening
    "L_afternoon",    # 1: L is shown in the afternoon
    "L_evening",      # 2: L is shown in the evening
    "M_morning",      # 3: M is shown in the morning
    "M_afternoon"     # 4: M is shown in the afternoon
]

# Helper functions for checking constraints
def check_negation(choice_idx):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    if choice_idx == 0:  # Negate "K in evening" -> K not in evening (i.e., afternoon)
        s_chk.add(Not(evening(pos["K"])))
    elif choice_idx == 1:  # Negate "L in afternoon" -> L not in afternoon
        s_chk.add(Not(afternoon(pos["L"])))
    elif choice_idx == 2:  # Negate "L in evening" -> L not in evening
        s_chk.add(Not(evening(pos["L"])))
    elif choice_idx == 3:  # Negate "M in morning" -> M not in morning
        s_chk.add(Not(morning(pos["M"])))
    elif choice_idx == 4:  # Negate "M in afternoon" -> M not in afternoon
        s_chk.add(Not(afternoon(pos["M"])))
    
    return s_chk.check() == unsat

# Check each answer choice
answer_index_list = []
for idx in range(len(answer_choices)):
    if check_negation(idx):
        answer_index_list.append(idx)

print(answer_index_list)