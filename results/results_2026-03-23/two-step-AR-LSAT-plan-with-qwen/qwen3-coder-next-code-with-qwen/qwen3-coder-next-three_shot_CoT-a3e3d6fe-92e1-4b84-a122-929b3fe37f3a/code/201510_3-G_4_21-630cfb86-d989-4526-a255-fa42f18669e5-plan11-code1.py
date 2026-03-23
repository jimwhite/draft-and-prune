from z3 import *

# Cookbook indices: K, L, M, N, O, P
cookbooks = ["K", "L", "M", "N", "O", "P"]

# Boolean variables: True = fall, False = spring
season_vars = {cb: Bool(f"{cb}_fall") for cb in cookbooks}

# Base solver
solver = Solver()

# Fixed assumption: N is published in the fall
solver.add(season_vars["N"] == True)

# M and P cannot be published in the same season
solver.add(season_vars["M"] != season_vars["P"])

# K and N must be published in the same season
solver.add(season_vars["K"] == season_vars["N"])

# If K is published in the fall, O must also be published in the fall
# Since N is fall and K == N, K is forced to fall, so O must be fall
solver.add(Implies(season_vars["K"], season_vars["O"]))

# If M is published in the fall, N must be published in the spring
# Since N is forced to fall, M cannot be fall (otherwise contradiction)
solver.add(Implies(season_vars["M"], Not(season_vars["N"])))

# Answer choices (as conditions to check for possibility)
answer_choices = [
    Not(season_vars["K"]),  # K is published in the spring
    season_vars["L"],       # L is published in the fall
    season_vars["M"],       # M is published in the fall
    Not(season_vars["O"]),  # O is published in the spring
    Not(season_vars["P"])   # P is published in the spring
]

# Check each answer choice
answer_index_list = []
for idx, condition in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(condition)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)