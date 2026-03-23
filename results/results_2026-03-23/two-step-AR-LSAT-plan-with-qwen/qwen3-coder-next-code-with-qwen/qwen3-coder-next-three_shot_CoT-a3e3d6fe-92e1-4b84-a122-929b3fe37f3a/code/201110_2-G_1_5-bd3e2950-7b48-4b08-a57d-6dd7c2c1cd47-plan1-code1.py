from z3 import *

# Employee indices: R=Robertson, S=Souza, T=Togowa, V=Vaughn, X=Xu, Y=Young
employees = ["R", "S", "T", "V", "X", "Y"]
pos = {e: Int(f"pos_{e}") for e in employees}

# Base solver
solver = Solver()

# Domain constraints: each position between 1 and 6, all distinct
for e in employees:
    solver.add(pos[e] >= 1, pos[e] <= 6)
solver.add(Distinct(*[pos[e] for e in employees]))

# Base ordering constraints
solver.add(pos["Y"] > pos["T"])  # Young > Togowa
solver.add(pos["X"] > pos["S"])  # Xu > Souza
solver.add(pos["R"] > pos["Y"])  # Robertson > Young
solver.add(pos["R"] <= 4)        # Robertson in {1,2,3,4}

# Conditional premise: Young > Souza
solver.add(pos["Y"] > pos["S"])

# Answer choices conditions
answer_conditions = [
    pos["T"] == 1,      # Togowa is assigned parking space #1
    pos["Y"] == 2,      # Young is assigned parking space #2
    pos["R"] == 3,      # Robertson is assigned parking space #3
    pos["S"] == 3,      # Souza is assigned parking space #3
    pos["V"] == 4       # Vaughn is assigned parking space #4
]

# Check each answer choice
answer_index_list = []
for idx, cond in enumerate(answer_conditions):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(cond)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)