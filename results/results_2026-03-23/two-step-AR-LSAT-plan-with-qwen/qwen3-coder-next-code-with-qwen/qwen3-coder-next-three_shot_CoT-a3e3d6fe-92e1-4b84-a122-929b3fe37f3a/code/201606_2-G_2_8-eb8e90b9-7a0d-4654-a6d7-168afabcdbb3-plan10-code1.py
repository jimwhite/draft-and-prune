from z3 import *

# Student indices: Louis=0, Mollie=1, Onyx=2, Ryan=3, Tiffany=4, Yoshio=5
# Year indices: 0->1921, 1->1922, 2->1923, 3->1924

assign = [Int(f"assign_{i}") for i in range(6)]

solver = Solver()

# Domain constraints: each student assigned to -1 (unassigned) or 0-3
for i in range(6):
    solver.add(Or([assign[i] == j for j in range(-1, 4)]))

# Exactly four students assigned
assigned_count = Sum([If(assign[i] >= 0, 1, 0) for i in range(6)])
solver.add(assigned_count == 4)

# One-to-one assignment: if two students are assigned, they get different years
for i in range(6):
    for j in range(i + 1, 6):
        solver.add(Or(assign[i] < 0, assign[j] < 0, assign[i] != assign[j]))

# 1923 constraint: only Louis (0) or Tiffany (4) can be assigned to year 2
for i in range(6):
    if i != 0 and i != 4:
        solver.add(assign[i] != 2)

# Mollie constraint: if assigned, must be to 1921 (0) or 1922 (1)
solver.add(Implies(assign[1] >= 0, Or(assign[1] == 0, assign[1] == 1)))

# Tiffany -> Ryan dependency: if Tiffany assigned, then Ryan must be assigned
solver.add(Implies(assign[4] >= 0, assign[3] >= 0))

# Ryan -> Onyx adjacency: if Ryan assigned to year r, then Onyx must be assigned to r-1
# This means Ryan cannot be assigned to 1921 (0), and Onyx must be assigned if Ryan is
solver.add(Implies(assign[3] >= 0, And(assign[2] == assign[3] - 1, assign[3] > 0)))

# Given assumption: Ryan and Yoshio are assigned
solver.add(assign[3] >= 0)
solver.add(assign[5] >= 0)

# Answer choices
answer_choices = [
    ("Louis is assigned to 1923.", assign[0] == 2),
    ("Mollie is assigned to 1921.", assign[1] == 0),
    ("Onyx is assigned to 1922.", assign[2] == 1),
    ("Tiffany is assigned to 1924.", assign[4] == 3),
    ("Yoshio is assigned to 1922.", assign[5] == 1)
]

# Check each choice
answer_index_list = []
for idx, (desc, condition) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(condition)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)