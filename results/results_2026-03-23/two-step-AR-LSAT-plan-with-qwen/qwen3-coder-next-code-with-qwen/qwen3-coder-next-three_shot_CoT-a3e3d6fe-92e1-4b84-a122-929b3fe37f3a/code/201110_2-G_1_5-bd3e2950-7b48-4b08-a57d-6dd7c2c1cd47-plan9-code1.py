from z3 import *

# Employee indices: 0-Robertson, 1-Souza, 2-Togowa, 3-Vaughn, 4-Xu, 5-Young
employees = ["Robertson", "Souza", "Togowa", "Vaughn", "Xu", "Young"]

# Create position variables for each employee
pos = {emp: Int(f"pos_{emp}") for emp in employees}

# Base solver
solver = Solver()

# Domain constraints: each position between 1 and 6
for emp in employees:
    solver.add(pos[emp] >= 1, pos[emp] <= 6)

# All-different constraint: each space used exactly once
solver.add(Distinct(*[pos[emp] for emp in employees]))

# Ordering constraints from rules
solver.add(pos["Young"] > pos["Togowa"])  # Young > Togowa
solver.add(pos["Xu"] > pos["Souza"])      # Xu > Souza
solver.add(pos["Robertson"] > pos["Young"])  # Robertson > Young
solver.add(pos["Robertson"] <= 4)         # Robertson in {1,2,3,4}

# Additional condition from question: Young > Souza
solver.add(pos["Young"] > pos["Souza"])

# Answer choices (as constraints to test)
answer_choices = [
    pos["Togowa"] == 1,      # Togowa is assigned parking space #1
    pos["Young"] == 2,       # Young is assigned parking space #2
    pos["Robertson"] == 3,   # Robertson is assigned parking space #3
    pos["Souza"] == 3,       # Souza is assigned parking space #3
    pos["Vaughn"] == 4       # Vaughn is assigned parking space #4
]

# Check each answer choice
answer_index_list = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    # Add base constraints + Young > Souza
    s_chk.add(solver.assertions())
    # Add the specific choice constraint
    s_chk.add(choice)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)