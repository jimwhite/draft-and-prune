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

# J must be shown in the evening (positions 6 or 7)
solver.add(Or(pos["J"] == 6, pos["J"] == 7))

# K cannot be shown in the morning (positions 1 or 2)
solver.add(And(pos["K"] != 1, pos["K"] != 2))

# L must be shown after K and before M: K < L < M
solver.add(pos["K"] < pos["L"])
solver.add(pos["L"] < pos["M"])

# Answer choices as logical conditions
answer_conditions = [
    # 0: K is shown in the evening (pos_K ∈ {6,7})
    Or(pos["K"] == 6, pos["K"] == 7),
    # 1: L is shown in the afternoon (pos_L ∈ {3,4,5})
    Or(pos["L"] == 3, pos["L"] == 4, pos["L"] == 5),
    # 2: L is shown in the evening (pos_L ∈ {6,7})
    Or(pos["L"] == 6, pos["L"] == 7),
    # 3: M is shown in the morning (pos_M ∈ {1,2})
    Or(pos["M"] == 1, pos["M"] == 2),
    # 4: M is shown in the afternoon (pos_M ∈ {3,4,5})
    Or(pos["M"] == 3, pos["M"] == 4, pos["M"] == 5)
]

# Check each answer choice by negation
correct_indices = []
for idx, cond in enumerate(answer_conditions):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add negation of the condition
    s_chk.add(Not(cond))
    
    if s_chk.check() == unsat:
        correct_indices.append(idx)

print(correct_indices)