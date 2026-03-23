from z3 import *

# Student indices: Louis=0, Mollie=1, Onyx=2, Ryan=3, Tiffany=4, Yoshio=5
students = ["Louis", "Mollie", "Onyx", "Ryan", "Tiffany", "Yoshio"]
assign = [Int(f"assign_{i}") for i in range(6)]

solver = Solver()

# Each student assigned to -1 (unassigned) or 0-3 (years 1921-1924)
for i in range(6):
    solver.add(Or(assign[i] == -1, And(assign[i] >= 0, assign[i] <= 3)))

# Exactly four students assigned
assigned_count = Sum([If(assign[i] != -1, 1, 0) for i in range(6)])
solver.add(assigned_count == 4)

# Years are unique among assigned students
year_vals = []
for i in range(6):
    year_var = Int(f"year_{i}")
    solver.add(year_var == If(assign[i] != -1, assign[i], 0))
    year_vals.append(year_var)
solver.add(Distinct(*year_vals))

# Fixed: Ryan and Yoshio are assigned
solver.add(assign[3] != -1)  # Ryan
solver.add(assign[5] != -1)  # Yoshio

# Only Louis or Tiffany can be assigned to 1923 (year index 2)
for i in range(6):
    solver.add(Implies(assign[i] == 2, Or(i == 0, i == 4)))

# Mollie constraint: if assigned, must be in year 0 or 1
solver.add(Implies(assign[1] != -1, Or(assign[1] == 0, assign[1] == 1)))

# Tiffany → Ryan constraint (Ryan is already assigned, so this holds trivially)
solver.add(Implies(assign[4] != -1, assign[3] != -1))

# Ryan → Onyx immediately prior constraint
# If Ryan is assigned to year y, then Onyx must be assigned to y-1 (so Ryan cannot be in 0)
solver.add(Implies(assign[3] != -1, assign[3] > 0))
solver.add(Implies(assign[3] != -1, assign[2] == assign[3] - 1))

# Since Ryan is assigned, Onyx must be assigned (by the above constraint)
solver.add(assign[2] != -1)

# Now test each answer choice
answer_choices = [
    ("Louis is assigned to 1923.", 0, 2),   # Louis (index 0) assigned to year 2
    ("Mollie is assigned to 1921.", 1, 0),  # Mollie (index 1) assigned to year 0
    ("Onyx is assigned to 1922.", 2, 1),    # Onyx (index 2) assigned to year 1
    ("Tiffany is assigned to 1924.", 4, 3), # Tiffany (index 4) assigned to year 3
    ("Yoshio is assigned to 1922.", 5, 1)   # Yoshio (index 5) assigned to year 1
]

answer_index_list = []
for idx, (_, student_idx, year_val) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add the specific claim: student assigned to year_val
    s_chk.add(assign[student_idx] == year_val)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)