from z3 import *

# Student indices: Louis=0, Mollie=1, Onyx=2, Ryan=3, Tiffany=4, Yoshio=5
# Year indices: 1921=0, 1922=1, 1923=2, 1924=3

students = ["Louis", "Mollie", "Onyx", "Ryan", "Tiffany", "Yoshio"]
years = [0, 1, 2, 3]  # 1921, 1922, 1923, 1924

# assign[i] = year assigned to student i, or -1 if not assigned
assign = [Int(f"assign_{i}") for i in range(6)]

solver = Solver()

# Domain constraints: each assigned student gets a year 0-3, unassigned get -1
for i in range(6):
    solver.add(Or(assign[i] == -1, And(assign[i] >= 0, assign[i] <= 3)))

# Exactly four students are assigned (4 non -1 values)
assigned_count = Sum([If(Not(assign[i] == -1), 1, 0) for i in range(6)])
solver.add(assigned_count == 4)

# Year uniqueness: assigned students must have distinct years
year_vars = [assign[i] for i in range(6)]
solver.add(Distinct(*[If(assign[i] == -1, -2, assign[i]) for i in range(6)]))

# Only Louis or Tiffany can be assigned to 1923 (year index 2)
solver.add(Implies(assign[0] == 2, True))  # Louis can be in 1923
solver.add(Implies(assign[4] == 2, True))  # Tiffany can be in 1923
solver.add(Implies(assign[1] == 2, False)) # Mollie cannot be in 1923
solver.add(Implies(assign[2] == 2, False)) # Onyx cannot be in 1923
solver.add(Implies(assign[3] == 2, False)) # Ryan cannot be in 1923
solver.add(Implies(assign[5] == 2, False)) # Yoshio cannot be in 1923

# Mollie implication: if assigned, must be in 1921 or 1922
solver.add(Implies(Not(assign[1] == -1), Or(assign[1] == 0, assign[1] == 1)))

# Tiffany implication: if assigned, then Ryan must be assigned
solver.add(Implies(Not(assign[4] == -1), Not(assign[3] == -1)))

# Ryan-Onyx adjacency: if Ryan is assigned, then Onyx must be assigned to year immediately prior
# This means: assign[Onyx] == assign[Ryan] - 1 AND assign[Ryan] > 0
solver.add(Implies(Not(assign[3] == -1), And(
    assign[2] == assign[3] - 1,
    assign[3] > 0
)))

# Scenario assumption: Ryan and Yoshio are assigned
solver.add(Not(assign[3] == -1))
solver.add(Not(assign[5] == -1))

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
for idx, (desc, constraint) in enumerate(answer_choices):
    s_chk = Solver()
    # Add all base constraints
    for a in solver.assertions():
        s_chk.add(a)
    # Add the specific choice constraint
    s_chk.add(constraint)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)