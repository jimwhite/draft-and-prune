from z3 import *

# House indices: J, K, L, M, N, O, P
houses = ["J", "K", "L", "M", "N", "O", "P"]
pos = {h: Int(f"pos_{h}") for h in houses}

# Base solver
solver = Solver()

# Domain constraints: positions are distinct integers from 1 to 7
for h in houses:
    solver.add(pos[h] >= 1, pos[h] <= 7)
solver.add(Distinct(*[pos[h] for h in houses]))

# Time-of-day constraints
def is_morning(p):
    return Or(p == 1, p == 2)

def is_afternoon(p):
    return And(p >= 3, p <= 5)

def is_evening(p):
    return Or(p == 6, p == 7)

# J must be shown in the evening
solver.add(is_evening(pos["J"]))

# K cannot be shown in the morning (i.e., not in positions 1 or 2)
solver.add(Not(is_morning(pos["K"])))

# L must be shown after K and before M: pos_K < pos_L < pos_M
solver.add(pos["K"] < pos["L"])
solver.add(pos["L"] < pos["M"])

# Answer choices (as logical conditions)
answer_conditions = [
    is_evening(pos["K"]),      # 0: K is shown in the evening
    is_afternoon(pos["L"]),    # 1: L is shown in the afternoon
    is_evening(pos["L"]),      # 2: L is shown in the evening
    pos["M"] <= 2,             # 3: M is shown in the morning
    And(pos["M"] >= 3, pos["M"] <= 5)  # 4: M is shown in the afternoon
]

# Check each answer choice to see if it must be true
answer_index_list = []
for idx, cond in enumerate(answer_conditions):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add the negation of the condition
    s_chk.add(Not(cond))
    
    # If UNSAT, then the original condition must be true
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

# Output the index of the correct answer (should be exactly one)
print(answer_index_list[0] if len(answer_index_list) == 1 else answer_index_list)