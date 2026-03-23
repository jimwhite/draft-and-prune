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

# Time-block constraints
# Morning: positions 1-2, Afternoon: 3-5, Evening: 6-7
# J must be in evening (positions 6 or 7)
solver.add(Or(pos["J"] == 6, pos["J"] == 7))

# K cannot be in morning (positions 1 or 2)
solver.add(And(pos["K"] != 1, pos["K"] != 2))

# Order constraints: L after K and before M
solver.add(pos["K"] < pos["L"])
solver.add(pos["L"] < pos["M"])

# Answer choices: check which must be true
answer_choices = [
    "K in evening",  # pos_K ∈ {6,7}
    "L in afternoon",  # pos_L ∈ {3,4,5}
    "L in evening",  # pos_L ∈ {6,7}
    "M in morning",  # pos_M ∈ {1,2}
    "M in afternoon"  # pos_M ∈ {3,4,5}
]

answer_index_list = []

# Check each answer choice by testing if its negation is UNSAT
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    if choice == "K in evening":
        # Negation: K not in evening → pos_K ∈ {3,4,5}
        s_chk.add(Or(pos["K"] == 3, pos["K"] == 4, pos["K"] == 5))
    elif choice == "L in afternoon":
        # Negation: L not in afternoon → pos_L ∈ {1,2,6,7}
        s_chk.add(Or(pos["L"] == 1, pos["L"] == 2, pos["L"] == 6, pos["L"] == 7))
    elif choice == "L in evening":
        # Negation: L not in evening → pos_L ∈ {1,2,3,4,5}
        s_chk.add(Or(pos["L"] == 1, pos["L"] == 2, pos["L"] == 3, pos["L"] == 4, pos["L"] == 5))
    elif choice == "M in morning":
        # Negation: M not in morning → pos_M ∈ {3,4,5,6,7}
        s_chk.add(Or(pos["M"] == 3, pos["M"] == 4, pos["M"] == 5, pos["M"] == 6, pos["M"] == 7))
    elif choice == "M in afternoon":
        # Negation: M not in afternoon → pos_M ∈ {1,2,6,7}
        s_chk.add(Or(pos["M"] == 1, pos["M"] == 2, pos["M"] == 6, pos["M"] == 7))
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)