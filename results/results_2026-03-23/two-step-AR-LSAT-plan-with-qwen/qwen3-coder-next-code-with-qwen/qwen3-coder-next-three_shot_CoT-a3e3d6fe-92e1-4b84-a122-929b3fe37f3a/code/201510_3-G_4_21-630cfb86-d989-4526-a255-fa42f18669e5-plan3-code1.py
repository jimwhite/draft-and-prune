from z3 import *

# Cookbooks: K, L, M, N, O, P
cookbooks = ["K", "L", "M", "N", "O", "P"]

# Boolean variables: cookbook_fall = True means published in fall
fall_vars = {c: Bool(f"{c}_fall") for c in cookbooks}

# Base solver
solver = Solver()

# Premise: N is published in the fall
solver.add(fall_vars["N"])

# M and P cannot be published in the same season
solver.add(fall_vars["M"] != fall_vars["P"])

# K and N must be published in the same season
solver.add(fall_vars["K"] == fall_vars["N"])

# If K is published in the fall, O must also be published in the fall
solver.add(Implies(fall_vars["K"], fall_vars["O"]))

# If M is published in the fall, N must be published in the spring
solver.add(Implies(fall_vars["M"], Not(fall_vars["N"])))

# Answer choices (as expressions)
answer_choices = [
    Not(fall_vars["K"]),      # K is published in the spring
    fall_vars["L"],           # L is published in the fall
    fall_vars["M"],           # M is published in the fall
    Not(fall_vars["O"]),      # O is published in the spring
    Not(fall_vars["P"])       # P is published in the spring
]

# Check each answer choice
answer_index_list = []
for idx, expr in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(expr)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)