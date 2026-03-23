from z3 import *

# House indices: J, K, L, M, N, O, P
houses = ["J", "K", "L", "M", "N", "O", "P"]
pos = {h: Int(f"pos_{h}") for h in houses}

# Base solver
solver = Solver()

# Domain constraints: positions 1-7
for h in houses:
    solver.add(pos[h] >= 1, pos[h] <= 7)

# Distinctness constraint
solver.add(Distinct(*[pos[h] for h in houses]))

# Time-slot constraints:
# Morning: positions 1-2, Afternoon: 3-5, Evening: 6-7
# J must be shown in the evening (positions 6 or 7)
solver.add(Or(pos["J"] == 6, pos["J"] == 7))

# K cannot be shown in the morning (positions 1 or 2)
solver.add(pos["K"] >= 3)

# Ordering constraint: L after K and before M
solver.add(pos["K"] < pos["L"], pos["L"] < pos["M"])

# Answer choices (as logical conditions)
answer_choices = [
    lambda: Or(pos["K"] == 6, pos["K"] == 7),  # K is shown in the evening
    lambda: And(pos["L"] >= 3, pos["L"] <= 5), # L is shown in the afternoon
    lambda: Or(pos["L"] == 6, pos["L"] == 7),  # L is shown in the evening
    lambda: Or(pos["M"] == 1, pos["M"] == 2),  # M is shown in the morning
    lambda: And(pos["M"] >= 3, pos["M"] <= 5)  # M is shown in the afternoon
]

# Check each answer choice for necessity (must be true)
answer_index_list = []
for idx, cond in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert the negation of the answer choice
    s_chk.add(Not(cond()))
    
    # If UNSAT, then the original condition must be true
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)