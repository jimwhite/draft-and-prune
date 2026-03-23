from z3 import *

# Cookbook indices: K, L, M, N, O, P
cookbooks = ["K", "L", "M", "N", "O", "P"]

# Boolean variables: cookbook_fall = True means published in fall
fall_vars = {c: Bool(f"{c}_fall") for c in cookbooks}

# Base solver
solver = Solver()

# Given condition: N is published in the fall
solver.add(fall_vars["N"])

# Constraint 1: M and P cannot be published in the same season
solver.add(fall_vars["M"] != fall_vars["P"])

# Constraint 2: K and N must be published in the same season
solver.add(fall_vars["K"] == fall_vars["N"])

# Constraint 3: If K is published in the fall, O must also be published in the fall
solver.add(Implies(fall_vars["K"], fall_vars["O"]))

# Constraint 4: If M is published in the fall, N must be published in the spring
solver.add(Implies(fall_vars["M"], Not(fall_vars["N"])))

# Answer choices (as logical conditions)
answer_choices = [
    Not(fall_vars["K"]),           # A. K is published in the spring
    fall_vars["L"],                # B. L is published in the fall
    fall_vars["M"],                # C. M is published in the fall
    Not(fall_vars["O"]),           # D. O is published in the spring
    fall_vars["P"]                 # E. P is published in the spring
]

# Check each answer choice
answer_index_list = []
for idx, cond in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(cond)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)