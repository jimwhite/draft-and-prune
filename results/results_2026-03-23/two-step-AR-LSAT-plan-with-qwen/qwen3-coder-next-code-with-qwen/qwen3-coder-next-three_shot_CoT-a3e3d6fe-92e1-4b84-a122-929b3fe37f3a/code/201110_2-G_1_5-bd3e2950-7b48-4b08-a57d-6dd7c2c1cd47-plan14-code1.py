from z3 import *

# Employee indices: Robertson=0, Souza=1, Togowa=2, Vaughn=3, Xu=4, Young=5
employees = ["Robertson", "Souza", "Togowa", "Vaughn", "Xu", "Young"]
pos = {e: Int(f"pos_{e}") for e in employees}

# Base solver
solver = Solver()

# Domain constraints: each position between 1 and 6
for e in employees:
    solver.add(pos[e] >= 1, pos[e] <= 6)

# Distinctness constraint
solver.add(Distinct(*[pos[e] for e in employees]))

# Base constraints (always true)
solver.add(pos["Young"] > pos["Togowa"])  # Young > Togowa
solver.add(pos["Xu"] > pos["Souza"])      # Xu > Souza
solver.add(pos["Robertson"] > pos["Young"])  # Robertson > Young
# Robertson ∈ {1,2,3,4}
solver.add(Or(pos["Robertson"] == 1, pos["Robertson"] == 2, pos["Robertson"] == 3, pos["Robertson"] == 4))

# Additional conditional constraint: Young > Souza
solver.add(pos["Young"] > pos["Souza"])

# Answer choices: A, B, C, D, E
answer_choices = [
    ("Togowa is assigned parking space #1.", pos["Togowa"] == 1),
    ("Young is assigned parking space #2.", pos["Young"] == 2),
    ("Robertson is assigned parking space #3.", pos["Robertson"] == 3),
    ("Souza is assigned parking space #3.", pos["Souza"] == 3),
    ("Vaughn is assigned parking space #4.", pos["Vaughn"] == 4)
]

# Check each answer choice
valid_indices = []
for idx, (desc, condition) in enumerate(answer_choices):
    s_chk = Solver()
    # Add all base constraints and conditional constraint
    for assertion in solver.assertions():
        s_chk.add(assertion)
    
    # Add the specific condition for this choice
    s_chk.add(condition)
    
    if s_chk.check() == sat:
        valid_indices.append(idx)

print(valid_indices)