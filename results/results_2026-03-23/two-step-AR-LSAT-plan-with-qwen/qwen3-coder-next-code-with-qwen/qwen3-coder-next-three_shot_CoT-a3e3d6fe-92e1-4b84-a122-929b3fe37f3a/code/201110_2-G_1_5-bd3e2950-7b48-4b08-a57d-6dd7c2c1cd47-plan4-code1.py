from z3 import *

# Employee indices: 0=Robertson, 1=Souza, 2=Togowa, 3=Vaughn, 4=Xu, 5=Young
pos = [Int(f"pos_{i}") for i in range(6)]

# Base solver
solver = Solver()

# Domain constraints: each position between 1 and 6
for i in range(6):
    solver.add(pos[i] >= 1, pos[i] <= 6)

# Uniqueness constraint
solver.add(Distinct(pos))

# Fixed constraints from base rules
# Young > Togowa: pos[5] > pos[2]
solver.add(pos[5] > pos[2])
# Xu > Souza: pos[4] > pos[1]
solver.add(pos[4] > pos[1])
# Robertson > Young: pos[0] > pos[5]
solver.add(pos[0] > pos[5])
# Robertson in {1,2,3,4}
solver.add(Or(pos[0] == 1, pos[0] == 2, pos[0] == 3, pos[0] == 4))

# Conditional premise: Young > Souza
solver.add(pos[5] > pos[1])

# Answer choices (indices correspond to the order in the problem)
answer_choices = [
    ("Togowa is assigned parking space #1.", 2, 1),   # pos[2] == 1
    ("Young is assigned parking space #2.", 5, 2),     # pos[5] == 2
    ("Robertson is assigned parking space #3.", 0, 3), # pos[0] == 3
    ("Souza is assigned parking space #3.", 1, 3),     # pos[1] == 3
    ("Vaughn is assigned parking space #4.", 3, 4)     # pos[3] == 4
]

# Check each answer choice
answer_index_list = []
for idx, (_, emp_idx, space) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add constraint for the specific choice
    s_chk.add(pos[emp_idx] == space)
    
    # If SAT, this choice could be true
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)