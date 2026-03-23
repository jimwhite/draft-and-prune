from z3 import *

# Employee variables: positions in [1,6]
employees = ["Robertson", "Souza", "Togowa", "Vaughn", "Xu", "Young"]
pos = {e: Int(f"pos_{e}") for e in employees}

# Base solver
solver = Solver()

# Domain constraints: each position between 1 and 6, all distinct
for e in employees:
    solver.add(pos[e] >= 1, pos[e] <= 6)
solver.add(Distinct(*[pos[e] for e in employees]))

# Base ordering constraints
solver.add(pos["Young"] > pos["Togowa"])
solver.add(pos["Xu"] > pos["Souza"])
solver.add(pos["Robertson"] > pos["Young"])
# Robertson in {1,2,3,4}
solver.add(Or(pos["Robertson"] == 1, pos["Robertson"] == 2, pos["Robertson"] == 3, pos["Robertson"] == 4))

# Extra condition for the scenario: Young > Souza
solver.add(pos["Young"] > pos["Souza"])

# Choices to check (indices correspond to the given list)
choices = [
    ("Togowa is assigned parking space #1.", pos["Togowa"] == 1),
    ("Young is assigned parking space #2.", pos["Young"] == 2),
    ("Robertson is assigned parking space #3.", pos["Robertson"] == 3),
    ("Souza is assigned parking space #3.", pos["Souza"] == 3),
    ("Vaughn is assigned parking space #4.", pos["Vaughn"] == 4)
]

# Check each choice
answer_index_list = []
for idx, (_, constraint) in enumerate(choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(constraint)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)