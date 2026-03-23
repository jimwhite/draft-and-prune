from z3 import *

# Student indices: Louis=0, Mollie=1, Onyx=2, Ryan=3, Tiffany=4, Yoshio=5
# Year indices: 1921=0, 1922=1, 1923=2, 1924=3

# Create assignment variables: assign[s] = year index (0-3) if assigned, -1 otherwise
assign = [Int(f"assign_{s}") for s in range(6)]

# Base solver
solver = Solver()

# Exactly four students are assigned (four have assign[s] != -1)
assigned_count = Sum([If(assign[s] != -1, 1, 0) for s in range(6)])
solver.add(assigned_count == 4)

# One-to-one constraint: each year has exactly one student
for y in range(4):
    # For each year, at most one student is assigned to it
    for s1 in range(6):
        for s2 in range(s1 + 1, 6):
            solver.add(Implies(
                And(assign[s1] == y, assign[s2] == y),
                False
            ))

# 1923 restriction: only Louis (0) or Tiffany (4) can be assigned to year 2
for s in range(6):
    if s not in [0, 4]:
        solver.add(Implies(assign[s] == 2, False))

# Mollie conditional: if assigned, must be to 1921 (0) or 1922 (1)
solver.add(Implies(assign[1] != -1, Or(assign[1] == 0, assign[1] == 1)))

# Tiffany-Ryan dependency: if Tiffany assigned, then Ryan must be assigned
solver.add(Implies(assign[4] != -1, assign[3] != -1))

# Ryan-Onyx dependency: if Ryan assigned, then Onyx must be assigned and immediately before
solver.add(Implies(assign[3] != -1, And(
    assign[2] != -1,
    assign[2] == assign[3] - 1
)))

# Scenario constraint: both Ryan and Yoshio are assigned
solver.add(assign[3] != -1)
solver.add(assign[5] != -1)

# Answer choices
answer_choices = [
    ("Louis is assigned to 1923.", assign[0] == 2),
    ("Mollie is assigned to 1921.", assign[1] == 0),
    ("Onyx is assigned to 1922.", assign[2] == 1),
    ("Tiffany is assigned to 1924.", assign[4] == 3),
    ("Yoshio is assigned to 1922.", assign[5] == 1)
]

# Check each answer choice
answer_index_list = []
for idx, (desc, condition) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(condition)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)