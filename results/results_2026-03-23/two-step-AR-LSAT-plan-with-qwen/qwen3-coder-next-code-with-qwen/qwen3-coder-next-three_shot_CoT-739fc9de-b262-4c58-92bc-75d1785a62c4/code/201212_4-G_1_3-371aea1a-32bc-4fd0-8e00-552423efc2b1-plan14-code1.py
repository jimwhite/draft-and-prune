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

# Time-slot constraints
def is_morning(p):
    return Or(p == 1, p == 2)

def is_afternoon(p):
    return Or(p == 3, p == 4, p == 5)

def is_evening(p):
    return Or(p == 6, p == 7)

# J must be shown in the evening
solver.add(is_evening(pos["J"]))

# K cannot be shown in the morning (i.e., position >= 3)
solver.add(pos["K"] >= 3)

# L after K and before M
solver.add(pos["K"] < pos["L"], pos["L"] < pos["M"])

# Answer choices
answer_choices = [
    "K is shown in the evening.",  # pos["K"] ∈ {6,7}
    "L is shown in the afternoon.",  # pos["L"] ∈ {3,4,5}
    "L is shown in the evening.",  # pos["L"] ∈ {6,7}
    "M is shown in the morning.",  # pos["M"] ∈ {1,2}
    "M is shown in the afternoon."  # pos["M"] ∈ {3,4,5}
]

# Check each answer choice (must be true)
answer_index_list = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Negate the choice
    if idx == 0:  # K is shown in evening → negation: K not in evening (i.e., morning or afternoon)
        s_chk.add(pos["K"] < 6)  # K not in {6,7} means pos_K <= 5
    elif idx == 1:  # L in afternoon → negation: L not in {3,4,5}
        s_chk.add(Or(pos["L"] == 1, pos["L"] == 2, pos["L"] >= 6))
    elif idx == 2:  # L in evening → negation: L not in {6,7}
        s_chk.add(pos["L"] <= 5)
    elif idx == 3:  # M in morning → negation: M not in {1,2}
        s_chk.add(pos["M"] >= 3)
    elif idx == 4:  # M in afternoon → negation: M not in {3,4,5}
        s_chk.add(Or(pos["M"] == 1, pos["M"] == 2, pos["M"] >= 6))
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)