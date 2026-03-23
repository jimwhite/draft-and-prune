from z3 import *

# Student indices: Louis=0, Mollie=1, Onyx=2, Ryan=3, Tiffany=4, Yoshio=5
students = ["Louis", "Mollie", "Onyx", "Ryan", "Tiffany", "Yoshio"]
student_idx = {s: i for i, s in enumerate(students)}

# Year indices: 1921=0, 1922=1, 1923=2, 1924=3
years = [0, 1, 2, 3]

# Assignment variables: assigned[i][y] = True if student i is assigned to year y
assigned = [[Bool(f"assigned_{students[i]}_{1921+y}") for y in years] for i in range(6)]

# Base solver
solver = Solver()

# Each year has exactly one student assigned
for y in years:
    solver.add(Sum([If(assigned[i][y], 1, 0) for i in range(6)]) == 1)

# Each student is assigned to at most one year
for i in range(6):
    solver.add(Sum([If(assigned[i][y], 1, 0) for y in years]) <= 1)

# Exactly four students are assigned (since there are four years)
solver.add(Sum([If(assigned[i][y], 1, 0) for i in range(6) for y in years]) == 4)

# Only Louis or Tiffany can be assigned to 1923 (year index 2)
for i in range(6):
    if i != student_idx["Louis"] and i != student_idx["Tiffany"]:
        solver.add(Not(assigned[i][2]))

# If Mollie is assigned, she must be in 1921 or 1922 (years 0 or 1)
# So Mollie cannot be assigned to 1923 (year 2) or 1924 (year 3)
solver.add(Not(assigned[student_idx["Mollie"]][2]))
solver.add(Not(assigned[student_idx["Mollie"]][3]))

# If Tiffany is assigned, then Ryan must be assigned
tiffany_assigned = Or(*[assigned[student_idx["Tiffany"]][y] for y in years])
ryan_assigned = Or(*[assigned[student_idx["Ryan"]][y] for y in years])
solver.add(Implies(tiffany_assigned, ryan_assigned))

# If Ryan is assigned, then Onyx must be assigned to the year immediately prior
for y in years:
    if y > 0:  # Ryan can be assigned to 1922, 1923, or 1924
        solver.add(Implies(assigned[student_idx["Ryan"]][y], assigned[student_idx["Onyx"]][y-1]))
    else:  # Ryan cannot be assigned to 1921 (no prior year)
        solver.add(Not(assigned[student_idx["Ryan"]][0]))

# Scenario constraint: both Ryan and Yoshio are assigned
solver.add(Or(*[assigned[student_idx["Ryan"]][y] for y in years]))
solver.add(Or(*[assigned[student_idx["Yoshio"]][y] for y in years]))

# Answer choices
answer_choices = [
    ("Louis is assigned to 1923.", student_idx["Louis"], 2),
    ("Mollie is assigned to 1921.", student_idx["Mollie"], 0),
    ("Onyx is assigned to 1922.", student_idx["Onyx"], 1),
    ("Tiffany is assigned to 1924.", student_idx["Tiffany"], 3),
    ("Yoshio is assigned to 1922.", student_idx["Yoshio"], 1)
]

# Check each choice
could_be_true_indices = []
for idx, (desc, student_i, year_y) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert the choice condition
    s_chk.add(assigned[student_i][year_y])
    
    if s_chk.check() == sat:
        could_be_true_indices.append(idx)

print(could_be_true_indices)