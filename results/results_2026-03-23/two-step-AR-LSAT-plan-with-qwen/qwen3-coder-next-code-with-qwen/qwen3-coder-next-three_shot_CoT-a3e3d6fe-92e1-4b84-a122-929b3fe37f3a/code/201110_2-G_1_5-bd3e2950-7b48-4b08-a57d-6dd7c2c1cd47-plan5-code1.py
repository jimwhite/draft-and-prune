from z3 import *

# Employee indices
employees = ["Robertson", "Souza", "Togowa", "Vaughn", "Xu", "Young"]
pos = {e: Int(f"pos_{e}") for e in employees}

# Base solver
solver = Solver()

# Domain constraints: each position between 1 and 6
for e in employees:
    solver.add(pos[e] >= 1, pos[e] <= 6)

# Distinctness constraint
solver.add(Distinct(*[pos[e] for e in employees]))

# Given ordering constraints
solver.add(pos["Young"] > pos["Togowa"])
solver.add(pos["Xu"] > pos["Souza"])
solver.add(pos["Robertson"] > pos["Young"])
# Robertson must be in {1,2,3,4}
solver.add(Or(pos["Robertson"] == 1, pos["Robertson"] == 2, pos["Robertson"] == 3, pos["Robertson"] == 4))

# Additional condition from question: Young > Souza
solver.add(pos["Young"] > pos["Souza"])

# Answer choices conditions
answer_conditions = [
    pos["Togowa"] == 1,           # A: Togowa is assigned parking space #1
    pos["Young"] == 2,            # B: Young is assigned parking space #2
    pos["Robertson"] == 3,        # C: Robertson is assigned parking space #3
    pos["Souza"] == 3,            # D: Souza is assigned parking space #3
    pos["Vaughn"] == 4            # E: Vaughn is assigned parking space #4
]

# Check each answer choice
answer_index_list = []
for idx, cond in enumerate(answer_conditions):
    s_chk = Solver()
    # Add base constraints + Young > Souza condition
    s_chk.add(solver.assertions())
    # Add the specific condition for this choice
    s_chk.add(cond)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)