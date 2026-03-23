from z3 import *

# House indices: J=0, K=1, L=2, M=3, N=4, O=5, P=6
houses = ["J", "K", "L", "M", "N", "O", "P"]
pos = {h: Int(f"pos_{h}") for h in houses}

# Base solver
solver = Solver()

# Domain constraints: positions 1-7, all distinct
for h in houses:
    solver.add(pos[h] >= 1, pos[h] <= 7)
solver.add(Distinct(*[pos[h] for h in houses]))

# Time-slot constraints
# Morning: positions 1-2, Afternoon: 3-5, Evening: 6-7

# J must be shown in the evening (positions 6 or 7)
solver.add(Or(pos["J"] == 6, pos["J"] == 7))

# K cannot be shown in the morning (positions 1 or 2)
solver.add(pos["K"] >= 3)

# L after K and before M: pos_K < pos_L < pos_M
solver.add(pos["K"] < pos["L"])
solver.add(pos["L"] < pos["M"])

# Answer choices (as conditions)
answer_conditions = [
    # 0: K is shown in the evening → pos_K ∈ {6,7}
    lambda s: Or(s["K"] == 6, s["K"] == 7),
    # 1: L is shown in the afternoon → pos_L ∈ {3,4,5}
    lambda s: Or(s["L"] == 3, s["L"] == 4, s["L"] == 5),
    # 2: L is shown in the evening → pos_L ∈ {6,7}
    lambda s: Or(s["L"] == 6, s["L"] == 7),
    # 3: M is shown in the morning → pos_M ∈ {1,2}
    lambda s: Or(s["M"] == 1, s["M"] == 2),
    # 4: M is shown in the afternoon → pos_M ∈ {3,4,5}
    lambda s: Or(s["M"] == 3, s["M"] == 4, s["M"] == 5)
]

must_be_true_list = []
for idx, cond in enumerate(answer_conditions):
    s_chk = Solver()
    # Add base constraints
    s_chk.add(solver.assertions())
    
    # Assert the negation of the condition
    s_chk.add(Not(cond(pos)))
    
    if s_chk.check() == unsat:
        must_be_true_list.append(idx)

print(must_be_true_list)