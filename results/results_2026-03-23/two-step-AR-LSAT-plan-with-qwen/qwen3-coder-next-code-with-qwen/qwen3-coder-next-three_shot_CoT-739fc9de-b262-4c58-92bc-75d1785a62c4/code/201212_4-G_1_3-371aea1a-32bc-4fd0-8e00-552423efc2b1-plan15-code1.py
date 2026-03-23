from z3 import *

# House position variables: pos_house = showing position (1-7)
houses = ["J", "K", "L", "M", "N", "O", "P"]
pos = {h: Int(f"pos_{h}") for h in houses}

# Base solver
solver = Solver()

# Domain constraints: each position between 1 and 7
for h in houses:
    solver.add(pos[h] >= 1, pos[h] <= 7)

# Uniqueness constraint: all positions distinct
solver.add(Distinct(*[pos[h] for h in houses]))

# J must be shown in the evening (positions 6 or 7)
solver.add(Or(pos["J"] == 6, pos["J"] == 7))

# K cannot be shown in the morning (positions 1-2)
solver.add(And(pos["K"] >= 3, pos["K"] <= 7))

# L after K and before M
solver.add(pos["K"] < pos["L"])
solver.add(pos["L"] < pos["M"])

# Answer choices (as conditions that must be true)
answer_choices = [
    "K in evening",  # K shown in positions 6 or 7
    "L in afternoon",  # L shown in positions 3, 4, or 5
    "L in evening",  # L shown in positions 6 or 7
    "M in morning",  # M shown in positions 1 or 2
    "M in afternoon"  # M shown in positions 3, 4, or 5
]

# Check each answer choice by testing if its negation is UNSAT
answer_index_list = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    if choice == "K in evening":
        # Negation: K not in evening → K in morning or afternoon (positions 1-5)
        s_chk.add(And(pos["K"] >= 1, pos["K"] <= 5))
    elif choice == "L in afternoon":
        # Negation: L not in afternoon → L in morning or evening (positions 1-2 or 6-7)
        s_chk.add(Or(pos["L"] == 1, pos["L"] == 2, pos["L"] == 6, pos["L"] == 7))
    elif choice == "L in evening":
        # Negation: L not in evening → L in morning or afternoon (positions 1-5)
        s_chk.add(And(pos["L"] >= 1, pos["L"] <= 5))
    elif choice == "M in morning":
        # Negation: M not in morning → M in afternoon or evening (positions 3-7)
        s_chk.add(And(pos["M"] >= 3, pos["M"] <= 7))
    elif choice == "M in afternoon":
        # Negation: M not in afternoon → M in morning or evening (positions 1-2 or 6-7)
        s_chk.add(Or(pos["M"] == 1, pos["M"] == 2, pos["M"] == 6, pos["M"] == 7))
    
    # If UNSAT, the answer choice must be true
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)