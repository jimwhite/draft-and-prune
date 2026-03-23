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

# Session constraints (implicit via position ranges)
# Morning: 1-2, Afternoon: 3-5, Evening: 6-7

# Given constraints
solver.add(pos["J"] >= 6)  # J in evening (positions 6 or 7)
solver.add(pos["K"] >= 3)  # K not in morning (positions 3-7)
solver.add(pos["K"] < pos["L"])  # L after K
solver.add(pos["L"] < pos["M"])  # L before M

# Answer choices (check which must be true)
answer_choices = [
    "K in evening",      # A: pos[K] >= 6
    "L in afternoon",    # B: 3 <= pos[L] <= 5
    "L in evening",      # C: pos[L] >= 6
    "M in morning",      # D: pos[M] <= 2
    "M in afternoon"     # E: 3 <= pos[M] <= 5
]

answer_index_list = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    if choice == "K in evening":
        # Negation: K not in evening (pos[K] < 6)
        s_chk.add(pos["K"] < 6)
    elif choice == "L in afternoon":
        # Negation: L not in afternoon (pos[L] < 3 or pos[L] > 5)
        s_chk.add(Or(pos["L"] < 3, pos["L"] > 5))
    elif choice == "L in evening":
        # Negation: L not in evening (pos[L] < 6)
        s_chk.add(pos["L"] < 6)
    elif choice == "M in morning":
        # Negation: M not in morning (pos[M] > 2)
        s_chk.add(pos["M"] > 2)
    elif choice == "M in afternoon":
        # Negation: M not in afternoon (pos[M] < 3 or pos[M] > 5)
        s_chk.add(Or(pos["M"] < 3, pos["M"] > 5))
    
    # If UNSAT under negation, then the original statement must be true
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)