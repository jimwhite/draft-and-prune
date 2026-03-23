from z3 import *

# Employee indices: [Robertson, Souza, Togowa, Vaughn, Xu, Young]
R, S, T, V, X, Y = 0, 1, 2, 3, 4, 5

# Position variables: pos[i] = parking space assigned to employee i (1-6)
pos = [Int(f"pos_{i}") for i in range(6)]

# Base solver
solver = Solver()

# Domain constraints: each position between 1 and 6
for i in range(6):
    solver.add(pos[i] >= 1, pos[i] <= 6)

# Distinctness constraint: all positions are different
solver.add(Distinct(pos))

# Base ordering constraints
solver.add(pos[Y] > pos[T])  # Young > Togowa
solver.add(pos[X] > pos[S])  # Xu > Souza
solver.add(pos[R] > pos[Y])  # Robertson > Young
solver.add(pos[R] <= 4)      # Robertson in {1,2,3,4}

# Conditional constraint: Young > Souza (given condition)
solver.add(pos[Y] > pos[S])

# Answer choices: each is a tuple (employee_index, space_number)
answer_choices = [
    (T, 1),  # Togowa is assigned parking space #1
    (Y, 2),  # Young is assigned parking space #2
    (R, 3),  # Robertson is assigned parking space #3
    (S, 3),  # Souza is assigned parking space #3
    (V, 4)   # Vaughn is assigned parking space #4
]

# Check each answer choice
answer_index_list = []
for idx, (emp, space) in enumerate(answer_choices):
    s_chk = Solver()
    # Add all base constraints and the conditional constraint
    s_chk.add(solver.assertions())
    # Add the specific assignment for this choice
    s_chk.add(pos[emp] == space)
    
    # If SAT, the statement could be true
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)