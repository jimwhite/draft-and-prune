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

# Session constraints:
# Morning: positions 1-2, Afternoon: positions 3-5, Evening: positions 6-7

# J must be shown in the evening (positions 6 or 7)
solver.add(Or(pos["J"] == 6, pos["J"] == 7))

# K cannot be shown in the morning (positions not 1 or 2)
solver.add(pos["K"] >= 3)

# L must be shown after K and before M: pos_K < pos_L < pos_M
solver.add(pos["K"] < pos["L"])
solver.add(pos["L"] < pos["M"])

# Answer choices (as logical statements)
answer_choices = [
    # 0: K is shown in the evening. (pos_K in {6,7})
    lambda s: Or(s["K"] == 6, s["K"] == 7),
    # 1: L is shown in the afternoon. (pos_L in {3,4,5})
    lambda s: Or(s["L"] == 3, s["L"] == 4, s["L"] == 5),
    # 2: L is shown in the evening. (pos_L in {6,7})
    lambda s: Or(s["L"] == 6, s["L"] == 7),
    # 3: M is shown in the morning. (pos_M in {1,2})
    lambda s: Or(s["M"] == 1, s["M"] == 2),
    # 4: M is shown in the afternoon. (pos_M in {3,4,5})
    lambda s: Or(s["M"] == 3, s["M"] == 4, s["M"] == 5)
]

must_be_true_choices = []

for idx, choice_func in enumerate(answer_choices):
    s_check = Solver()
    # Add all base constraints
    s_check.add(solver.assertions())
    
    # Assert the negation of the choice statement
    s_check.add(Not(choice_func(pos)))
    
    # If UNSAT, then the choice must be true
    if s_check.check() == unsat:
        must_be_true_choices.append(idx)

print(must_be_true_choices)