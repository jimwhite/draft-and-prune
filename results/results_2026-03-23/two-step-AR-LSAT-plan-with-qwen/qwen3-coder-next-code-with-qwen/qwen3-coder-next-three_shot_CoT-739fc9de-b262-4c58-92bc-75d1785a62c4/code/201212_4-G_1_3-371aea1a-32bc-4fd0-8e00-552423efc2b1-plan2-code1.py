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

# Time slot constraints
# Morning: positions 1-2, Afternoon: 3-5, Evening: 6-7

# J must be in evening (positions 6 or 7)
solver.add(Or(pos["J"] == 6, pos["J"] == 7))

# K cannot be in morning (not positions 1 or 2)
solver.add(pos["K"] >= 3)

# L after K and before M: K < L < M
solver.add(pos["K"] < pos["L"])
solver.add(pos["L"] < pos["M"])

# Answer choices (as logical conditions that must be true)
# 0: "K is shown in the evening" → pos_K ∈ {6,7}
# 1: "L is shown in the afternoon" → pos_L ∈ {3,4,5}
# 2: "L is shown in the evening" → pos_L ∈ {6,7}
# 3: "M is shown in the morning" → pos_M ∈ {1,2}
# 4: "M is shown in the afternoon" → pos_M ∈ {3,4,5}

must_be_true_flags = []

for idx in range(5):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    if idx == 0:  # K in evening is false → pos_K ∉ {6,7} → pos_K <= 5
        s_chk.add(pos["K"] <= 5)
    elif idx == 1:  # L in afternoon is false → pos_L ∉ {3,4,5} → pos_L ∈ {1,2,6,7}
        s_chk.add(Or(pos["L"] == 1, pos["L"] == 2, pos["L"] == 6, pos["L"] == 7))
    elif idx == 2:  # L in evening is false → pos_L ∉ {6,7} → pos_L ∈ {1,2,3,4,5}
        s_chk.add(Or(pos["L"] == 1, pos["L"] == 2, pos["L"] == 3, pos["L"] == 4, pos["L"] == 5))
    elif idx == 3:  # M in morning is false → pos_M ∉ {1,2} → pos_M >= 3
        s_chk.add(pos["M"] >= 3)
    elif idx == 4:  # M in afternoon is false → pos_M ∉ {3,4,5} → pos_M ∈ {1,2,6,7}
        s_chk.add(Or(pos["M"] == 1, pos["M"] == 2, pos["M"] == 6, pos["M"] == 7))
    
    if s_chk.check() == unsat:
        must_be_true_flags.append(True)
    else:
        must_be_true_flags.append(False)

# Output the index of the only statement that must be true
result_indices = [i for i, flag in enumerate(must_be_true_flags) if flag]
print(result_indices[0] if result_indices else -1)