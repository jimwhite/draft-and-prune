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

# Session constraints based on position ranges
# Morning: 1-2, Afternoon: 3-5, Evening: 6-7

# J must be shown in the evening (positions 6 or 7)
solver.add(Or(pos["J"] == 6, pos["J"] == 7))

# K cannot be shown in the morning (not positions 1 or 2)
solver.add(pos["K"] >= 3)

# L is shown after K and before M
solver.add(pos["K"] < pos["L"], pos["L"] < pos["M"])

# Answer choices (as logical propositions)
answer_choices = [
    # "K is shown in the evening" ⇔ pos["K"] ∈ {6, 7}
    lambda s: Or(s["K"] == 6, s["K"] == 7),
    # "L is shown in the afternoon" ⇔ pos["L"] ∈ {3, 4, 5}
    lambda s: Or(s["L"] == 3, s["L"] == 4, s["L"] == 5),
    # "L is shown in the evening" ⇔ pos["L"] ∈ {6, 7}
    lambda s: Or(s["L"] == 6, s["L"] == 7),
    # "M is shown in the morning" ⇔ pos["M"] ∈ {1, 2}
    lambda s: Or(s["M"] == 1, s["M"] == 2),
    # "M is shown in the afternoon" ⇔ pos["M"] ∈ {3, 4, 5}
    lambda s: Or(s["M"] == 3, s["M"] == 4, s["M"] == 5)
]

# Check each choice using proof by contradiction
answer_index_list = []
for idx, prop in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert the choice is false (negation of the proposition)
    s_chk.add(Not(prop(pos)))
    
    # If UNSAT, then the choice must be true
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)