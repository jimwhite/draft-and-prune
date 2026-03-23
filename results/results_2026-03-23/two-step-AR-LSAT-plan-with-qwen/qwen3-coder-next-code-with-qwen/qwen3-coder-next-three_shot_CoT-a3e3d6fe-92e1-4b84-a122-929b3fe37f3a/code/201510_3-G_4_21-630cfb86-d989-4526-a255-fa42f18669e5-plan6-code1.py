from z3 import *

# Cookbooks: K, L, M, N, O, P
cookbooks = ["K", "L", "M", "N", "O", "P"]

# Boolean variables: cookbook_fall = True if published in fall, False if spring
cookbook_fall = {cb: Bool(f"{cb}_fall") for cb in cookbooks}

# Base solver
solver = Solver()

# Constraint 1: M and P cannot be published in the same season
solver.add(cookbook_fall["M"] != cookbook_fall["P"])

# Constraint 2: K and N must be published in the same season
solver.add(cookbook_fall["K"] == cookbook_fall["N"])

# Constraint 3: If K is published in the fall, O must also be published in the fall
solver.add(Or(Not(cookbook_fall["K"]), cookbook_fall["O"]))

# Constraint 4: If M is published in the fall, N must be published in the spring
solver.add(Or(Not(cookbook_fall["M"]), Not(cookbook_fall["N"])))

# Premise: N is published in the fall
solver.add(cookbook_fall["N"] == True)

# Answer choices (as parsed, note '0' is likely a typo for 'O')
answer_choices = [
    ("K is published in the spring.", Not(cookbook_fall["K"])),
    ("L is published in the fall.", cookbook_fall["L"]),
    ("M is published in the fall.", cookbook_fall["M"]),
    ("O is published in the spring.", Not(cookbook_fall["O"])),
    ("P is published in the spring.", Not(cookbook_fall["P"]))
]

# Check each answer choice
answer_index_list = []
for idx, (_, assertion) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(assertion)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)