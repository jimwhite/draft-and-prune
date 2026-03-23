from z3 import *

# Student indices: Louis, Mollie, Onyx, Ryan, Tiffany, Yoshio
students = ["Louis", "Mollie", "Onyx", "Ryan", "Tiffany", "Yoshio"]
student_indices = {s: i for i, s in enumerate(students)}

# Years as integers: 1921=0, 1922=1, 1923=2, 1924=3
years = [0, 1, 2, 3]  # representing 1921, 1922, 1923, 1924

# Create assignment variables: assign[i] = year index (0-3) if student i is assigned, -1 if not assigned
assign = [Int(f"assign_{s}") for s in students]

# Base solver
solver = Solver()

# Each student is either assigned to a year (0-3) or not assigned (-1)
for i in range(6):
    solver.add(Or([assign[i] == y for y in years] + [assign[i] == -1]))

# Exactly 4 students are assigned
assigned_count = Sum([If(assign[i] != -1, 1, 0) for i in range(6)])
solver.add(assigned_count == 4)

# The assigned years are exactly {0,1,2,3} (all distinct and cover all years)
# First ensure no duplicate years among assigned students
year_vars = []
for i in range(6):
    year_vars.append(If(assign[i] != -1, assign[i], 4))  # use 4 as dummy for unassigned
solver.add(Distinct(*year_vars))

# Only Louis or Tiffany can be assigned to 1923 (year index 2)
for i, s in enumerate(students):
    if s not in ["Louis", "Tiffany"]:
        solver.add(Implies(assign[i] != -1, assign[i] != 2))

# If Mollie is assigned, then she must be assigned to either 1921 or 1922 (years 0 or 1)
mollie_idx = student_indices["Mollie"]
solver.add(Implies(assign[mollie_idx] != -1, Or(assign[mollie_idx] == 0, assign[mollie_idx] == 1)))

# If Tiffany is assigned, then Ryan must be assigned
tiffany_idx = student_indices["Tiffany"]
ryan_idx = student_indices["Ryan"]
solver.add(Implies(assign[tiffany_idx] != -1, assign[ryan_idx] != -1))

# If Ryan is assigned, then Onyx must be assigned and Onyx's year is immediately prior to Ryan's
onyx_idx = student_indices["Onyx"]
solver.add(Implies(assign[ryan_idx] != -1, 
                   And(assign[onyx_idx] != -1,
                       assign[onyx_idx] == assign[ryan_idx] - 1)))

# Problem-specific assumption: both Ryan and Yoshio are assigned
yoshio_idx = student_indices["Yoshio"]
solver.add(assign[ryan_idx] != -1)
solver.add(assign[yoshio_idx] != -1)

# Answer choices
answer_choices = [
    ("Louis is assigned to 1923.", lambda: assign[student_indices["Louis"]] == 2),
    ("Mollie is assigned to 1921.", lambda: assign[mollie_idx] == 0),
    ("Onyx is assigned to 1922.", lambda: assign[onyx_idx] == 1),
    ("Tiffany is assigned to 1924.", lambda: assign[tiffany_idx] == 3),
    ("Yoshio is assigned to 1922.", lambda: assign[yoshio_idx] == 1)
]

# Check each answer choice
answer_index_list = []
for idx, (desc, constraint_func) in enumerate(answer_choices):
    s_chk = Solver()
    # Add all base constraints plus Ryan and Yoshio assigned
    for a in solver.assertions():
        s_chk.add(a)
    
    # Add the specific choice constraint
    s_chk.add(constraint_func())
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)