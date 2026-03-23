from z3 import *

# Employee indices: Robertson=0, Souza=1, Togowa=2, Vaughn=3, Xu=4, Young=5
employees = ["Robertson", "Souza", "Togowa", "Vaughn", "Xu", "Young"]
pos = {e: Int(f"pos_{e}") for e in employees}

# Base solver
solver = Solver()

# Domain constraints: each position between 1 and 6, all distinct
for e in employees:
    solver.add(pos[e] >= 1, pos[e] <= 6)
solver.add(Distinct(*[pos[e] for e in employees]))

# Base constraints from rules
solver.add(pos["Young"] > pos["Togowa"])  # Young > Togowa
solver.add(pos["Xu"] > pos["Souza"])      # Xu > Souza
solver.add(pos["Robertson"] > pos["Young"])  # Robertson > Young
solver.add(Or(pos["Robertson"] == 1, pos["Robertson"] == 2, pos["Robertson"] == 3, pos["Robertson"] == 4))

# Conditional constraint: Young > Souza
solver.add(pos["Young"] > pos["Souza"])

# Answer choices
answer_choices = [
    ("Togowa is assigned parking space #1.", pos["Togowa"] == 1),
    ("Young is assigned parking space #2.", pos["Young"] == 2),
    ("Robertson is assigned parking space #3.", pos["Robertson"] == 3),
    ("Souza is assigned parking space #3.", pos["Souza"] == 3),
    ("Vaughn is assigned parking space #4.", pos["Vaughn"] == 4)
]

# Check each answer choice
satisfiable_indices = []
for idx, (_, constraint) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(constraint)
    
    if s_chk.check() == sat:
        satisfiable_indices.append(idx)

# Output the index of the first (and only) satisfiable choice
print(satisfiable_indices[0] if satisfiable_indices else -1)