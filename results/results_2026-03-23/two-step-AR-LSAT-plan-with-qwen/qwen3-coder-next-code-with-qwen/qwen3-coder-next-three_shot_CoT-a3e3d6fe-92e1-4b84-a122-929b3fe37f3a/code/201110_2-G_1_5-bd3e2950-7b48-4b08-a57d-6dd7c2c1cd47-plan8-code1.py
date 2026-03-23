from z3 import *

# Employee indices: 0-Robertson, 1-Souza, 2-Togowa, 3-Vaughn, 4-Xu, 5-Young
employees = ["Robertson", "Souza", "Togowa", "Vaughn", "Xu", "Young"]

# Create integer variables for each employee's parking space (1-6)
spaces = [Int(f"space_{emp}") for emp in employees]

# Base solver
solver = Solver()

# Domain constraints: each space between 1 and 6
for s in spaces:
    solver.add(s >= 1, s <= 6)

# All spaces distinct
solver.add(Distinct(spaces))

# Ordering constraints from rules:
# Young > Togowa (index 5 > index 2)
solver.add(spaces[5] > spaces[2])
# Xu > Souza (index 4 > index 1)
solver.add(spaces[4] > spaces[1])
# Robertson > Young (index 0 > index 5)
solver.add(spaces[0] > spaces[5])
# Robertson ∈ {1,2,3,4}
solver.add(Or(spaces[0] == 1, spaces[0] == 2, spaces[0] == 3, spaces[0] == 4))

# Extra conditional constraint: Young > Souza (index 5 > index 1)
solver.add(spaces[5] > spaces[1])

# Answer choices (each as a constraint that the statement is true)
answer_choices = [
    spaces[2] == 1,  # Togowa is assigned parking space #1
    spaces[5] == 2,  # Young is assigned parking space #2
    spaces[0] == 3,  # Robertson is assigned parking space #3
    spaces[1] == 3,  # Souza is assigned parking space #3
    spaces[3] == 4   # Vaughn is assigned parking space #4
]

# Check each answer choice
answer_index_list = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(choice)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)