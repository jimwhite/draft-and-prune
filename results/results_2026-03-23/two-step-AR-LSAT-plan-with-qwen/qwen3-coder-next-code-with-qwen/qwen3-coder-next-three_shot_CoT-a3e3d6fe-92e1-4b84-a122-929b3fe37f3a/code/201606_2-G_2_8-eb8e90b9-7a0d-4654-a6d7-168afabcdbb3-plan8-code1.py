from z3 import *

# Student indices: Louis=0, Mollie=1, Onyx=2, Ryan=3, Tiffany=4, Yoshio=5
# Year indices: 1921=0, 1922=1, 1923=2, 1924=3

assign = [Int(f"assign_{i}") for i in range(6)]

solver = Solver()

# Domain constraints: each student assigned to -1 (not assigned) or 0-3
for i in range(6):
    solver.add(Or([assign[i] == j for j in range(-1, 4)]))

# Exactly four students are assigned
assigned_count = Sum([If(assign[i] != -1, 1, 0) for i in range(6)])
solver.add(assigned_count == 4)

# One-to-one mapping: assigned students get distinct years
solver.add(Distinct([assign[i] for i in range(6) if True]))

# Year 1923 constraint: only Louis (0) or Tiffany (4)
for i in range(6):
    solver.add(Implies(assign[i] == 2, Or(i == 0, i == 4)))

# Mollie constraint: if assigned, must be in year 0 or 1
solver.add(Implies(assign[1] != -1, Or(assign[1] == 0, assign[1] == 1)))

# Tiffany-Ryan dependency: if Tiffany assigned, then Ryan must be assigned
solver.add(Implies(assign[4] != -1, assign[3] != -1))

# Ryan-Onyx adjacency: if Ryan assigned, then Onyx must be assigned to year immediately prior
# This implies Ryan cannot be in year 0 (1921)
solver.add(Implies(assign[3] != -1, And(
    assign[2] != -1,
    assign[2] == assign[3] - 1,
    assign[3] >= 1
)))

# Scenario constraint: both Ryan and Yoshio are assigned
solver.add(assign[3] != -1)
solver.add(assign[5] != -1)

# Choices
choices = [
    ("Louis is assigned to 1923.", lambda: assign[0] == 2),
    ("Mollie is assigned to 1921.", lambda: assign[1] == 0),
    ("Onyx is assigned to 1922.", lambda: assign[2] == 1),
    ("Tiffany is assigned to 1924.", lambda: assign[4] == 3),
    ("Yoshio is assigned to 1922.", lambda: assign[5] == 1)
]

answer_index_list = []
for idx, (desc, constraint_func) in enumerate(choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(constraint_func())
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)