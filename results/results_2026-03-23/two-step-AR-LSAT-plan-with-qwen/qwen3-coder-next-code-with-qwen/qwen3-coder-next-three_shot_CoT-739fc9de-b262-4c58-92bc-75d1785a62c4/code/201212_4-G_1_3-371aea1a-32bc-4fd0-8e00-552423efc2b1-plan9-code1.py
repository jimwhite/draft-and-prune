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

# Time-of-day constraints
# Morning: positions 1-2, Afternoon: 3-5, Evening: 6-7
# J must be in evening: pos[J] >= 6
solver.add(pos["J"] >= 6)
# K cannot be in morning: pos[K] >= 3
solver.add(pos["K"] >= 3)

# Ordering constraints: L after K, L before M
solver.add(pos["L"] > pos["K"])
solver.add(pos["L"] < pos["M"])

# Answer choices (as logical statements)
# A: K in evening → pos[K] >= 6
# B: L in afternoon → 3 <= pos[L] <= 5
# C: L in evening → pos[L] >= 6
# D: M in morning → pos[M] <= 2
# E: M in afternoon → 3 <= pos[M] <= 5

answer_choices = [
    lambda s: s[pos["K"]] >= 6,                    # A
    lambda s: And(s[pos["L"]] >= 3, s[pos["L"]] <= 5),  # B
    lambda s: s[pos["L"]] >= 6,                    # C
    lambda s: s[pos["M"]] <= 2,                    # D
    lambda s: And(s[pos["M"]] >= 3, s[pos["M"]] <= 5)   # E
]

answer_index_list = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert the negation of the choice
    if idx == 0:  # A: K in evening → negation is pos[K] <= 5
        s_chk.add(pos["K"] <= 5)
    elif idx == 1:  # B: L in afternoon → negation is pos[L] < 3 or pos[L] > 5
        s_chk.add(Or(pos["L"] < 3, pos["L"] > 5))
    elif idx == 2:  # C: L in evening → negation is pos[L] <= 5
        s_chk.add(pos["L"] <= 5)
    elif idx == 3:  # D: M in morning → negation is pos[M] >= 3
        s_chk.add(pos["M"] >= 3)
    elif idx == 4:  # E: M in afternoon → negation is pos[M] < 3 or pos[M] > 5
        s_chk.add(Or(pos["M"] < 3, pos["M"] > 5))
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)