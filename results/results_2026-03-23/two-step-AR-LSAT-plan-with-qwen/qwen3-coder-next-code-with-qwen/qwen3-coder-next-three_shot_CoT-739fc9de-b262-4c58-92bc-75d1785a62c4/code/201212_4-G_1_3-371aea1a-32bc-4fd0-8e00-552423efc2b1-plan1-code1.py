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

# Session constraints:
# Morning: positions 1-2, Afternoon: 3-5, Evening: 6-7
# J must be in evening (positions 6 or 7)
solver.add(Or(pos["J"] == 6, pos["J"] == 7))

# K cannot be in morning (positions 1 or 2)
solver.add(And(pos["K"] != 1, pos["K"] != 2))

# L after K and before M: pos[K] < pos[L] < pos[M]
solver.add(pos["K"] < pos["L"])
solver.add(pos["L"] < pos["M"])

# Answer choices (indices correspond to the given list)
# A: K is shown in evening → pos[K] ∈ {6,7}
# B: L is shown in afternoon → pos[L] ∈ {3,4,5}
# C: L is shown in evening → pos[L] ∈ {6,7}
# D: M is shown in morning → pos[M] ∈ {1,2}
# E: M is shown in afternoon → pos[M] ∈ {3,4,5}

answer_index_list = []

# Check A: "K is shown in the evening"
s_chk = Solver()
s_chk.add(solver.assertions())
# Negation: K is NOT in evening → pos[K] ≤ 5
s_chk.add(pos["K"] <= 5)
if s_chk.check() == unsat:
    answer_index_list.append(0)

# Check B: "L is shown in the afternoon"
s_chk = Solver()
s_chk.add(solver.assertions())
# Negation: L is NOT in afternoon → pos[L] ∈ {1,2} or pos[L] ∈ {6,7}
s_chk.add(Or(pos["L"] == 1, pos["L"] == 2, pos["L"] == 6, pos["L"] == 7))
if s_chk.check() == unsat:
    answer_index_list.append(1)

# Check C: "L is shown in the evening"
s_chk = Solver()
s_chk.add(solver.assertions())
# Negation: L is NOT in evening → pos[L] ≤ 5
s_chk.add(pos["L"] <= 5)
if s_chk.check() == unsat:
    answer_index_list.append(2)

# Check D: "M is shown in the morning"
s_chk = Solver()
s_chk.add(solver.assertions())
# Negation: M is NOT in morning → pos[M] ≥ 3
s_chk.add(pos["M"] >= 3)
if s_chk.check() == unsat:
    answer_index_list.append(3)

# Check E: "M is shown in the afternoon"
s_chk = Solver()
s_chk.add(solver.assertions())
# Negation: M is NOT in afternoon → pos[M] ∈ {1,2} or pos[M] ∈ {6,7}
s_chk.add(Or(pos["M"] == 1, pos["M"] == 2, pos["M"] == 6, pos["M"] == 7))
if s_chk.check() == unsat:
    answer_index_list.append(4)

print(answer_index_list)