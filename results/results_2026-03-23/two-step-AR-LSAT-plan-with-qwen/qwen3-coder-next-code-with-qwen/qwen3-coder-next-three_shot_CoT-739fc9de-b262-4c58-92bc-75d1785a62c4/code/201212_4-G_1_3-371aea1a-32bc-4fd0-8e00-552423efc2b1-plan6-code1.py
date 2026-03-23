from z3 import *

# House indices: J, K, L, M, N, O, P
houses = ["J", "K", "L", "M", "N", "O", "P"]

# Position variables (1-indexed: 1 to 7)
pos = {h: Int(f"pos_{h}") for h in houses}

# Base solver
solver = Solver()

# Domain constraints: each house assigned a unique position from 1 to 7
for h in houses:
    solver.add(pos[h] >= 1, pos[h] <= 7)
solver.add(Distinct(*[pos[h] for h in houses]))

# Time slot constraints
def is_morning(p):
    return Or(p == 1, p == 2)

def is_afternoon(p):
    return Or(p == 3, p == 4, p == 5)

def is_evening(p):
    return Or(p == 6, p == 7)

# J must be shown in the evening
solver.add(is_evening(pos["J"]))

# K cannot be shown in the morning (so afternoon or evening)
solver.add(Not(is_morning(pos["K"])))

# L after K and before M
solver.add(pos["K"] < pos["L"], pos["L"] < pos["M"])

# Answer choices
answer_choices = [
    ("K is shown in the evening.", lambda: is_evening(pos["K"])),
    ("L is shown in the afternoon.", lambda: is_afternoon(pos["L"])),
    ("L is shown in the evening.", lambda: is_evening(pos["L"])),
    ("M is shown in the morning.", lambda: is_morning(pos["M"])),
    ("M is shown in the afternoon.", lambda: is_afternoon(pos["M"]))
]

# Check each answer choice
answer_index_list = []
for idx, (desc, condition) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add negation of the condition
    cond_expr = condition()
    s_chk.add(Not(cond_expr))
    
    # If UNSAT, then the original condition must be true
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

# Output the index of the correct choice
print(answer_index_list[0] if answer_index_list else -1)