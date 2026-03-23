from z3 import *

# Employee indices: 0: Robertson, 1: Souza, 2: Togowa, 3: Vaughn, 4: Xu, 5: Young
employees = ["Robertson", "Souza", "Togowa", "Vaughn", "Xu", "Young"]
pos = {emp: Int(f"pos_{emp}") for emp in employees}

# Base solver
solver = Solver()

# Domain constraints: each position between 1 and 6
for emp in employees:
    solver.add(pos[emp] >= 1, pos[emp] <= 6)

# All positions distinct
solver.add(Distinct(*[pos[emp] for emp in employees]))

# Basic ordering constraints
solver.add(pos["Young"] > pos["Togowa"])  # Young > Togowa
solver.add(pos["Xu"] > pos["Souza"])      # Xu > Souza
solver.add(pos["Robertson"] > pos["Young"])  # Robertson > Young
solver.add(pos["Robertson"] <= 4)         # Robertson in {1,2,3,4}

# Conditional assumption: Young > Souza
solver.add(pos["Young"] > pos["Souza"])

# Answer choices: list of (description, constraint)
answer_choices = [
    ("Togowa is assigned parking space #1.", pos["Togowa"] == 1),
    ("Young is assigned parking space #2.", pos["Young"] == 2),
    ("Robertson is assigned parking space #3.", pos["Robertson"] == 3),
    ("Souza is assigned parking space #3.", pos["Souza"] == 3),
    ("Vaughn is assigned parking space #4.", pos["Vaughn"] == 4)
]

# Check each answer choice
answer_index_list = []
for idx, (_, constraint) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(constraint)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)