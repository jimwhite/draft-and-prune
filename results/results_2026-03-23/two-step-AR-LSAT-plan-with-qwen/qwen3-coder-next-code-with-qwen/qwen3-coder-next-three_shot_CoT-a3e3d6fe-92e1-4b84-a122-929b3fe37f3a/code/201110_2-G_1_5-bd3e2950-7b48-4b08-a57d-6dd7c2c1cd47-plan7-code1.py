from z3 import *

# Employee indices: Robertson=0, Souza=1, Togowa=2, Vaughn=3, Xu=4, Young=5
employees = ["Robertson", "Souza", "Togowa", "Vaughn", "Xu", "Young"]
pos = [Int(f"pos_{emp}") for emp in employees]

# Base solver
solver = Solver()

# Domain constraints: each position between 1 and 6
for p in pos:
    solver.add(p >= 1, p <= 6)

# Distinctness constraint
solver.add(Distinct(pos))

# Base ordering constraints
# Young > Togowa
solver.add(pos[5] > pos[2])
# Xu > Souza
solver.add(pos[4] > pos[1])
# Robertson > Young
solver.add(pos[0] > pos[5])
# Robertson ∈ {1,2,3,4}
solver.add(pos[0] <= 4)

# Hypothetical condition: Young > Souza
solver.add(pos[5] > pos[1])

# Answer choices (indices 0-4)
answer_choices = [
    ("Togowa is assigned parking space #1.", pos[2] == 1),
    ("Young is assigned parking space #2.", pos[5] == 2),
    ("Robertson is assigned parking space #3.", pos[0] == 3),
    ("Souza is assigned parking space #3.", pos[1] == 3),
    ("Vaughn is assigned parking space #4.", pos[3] == 4)
]

# Check each answer choice
valid_indices = []
for idx, (_, constraint) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(constraint)
    
    if s_chk.check() == sat:
        valid_indices.append(idx)

# Print the index of the valid choice (only one expected)
print(valid_indices[0] if valid_indices else -1)