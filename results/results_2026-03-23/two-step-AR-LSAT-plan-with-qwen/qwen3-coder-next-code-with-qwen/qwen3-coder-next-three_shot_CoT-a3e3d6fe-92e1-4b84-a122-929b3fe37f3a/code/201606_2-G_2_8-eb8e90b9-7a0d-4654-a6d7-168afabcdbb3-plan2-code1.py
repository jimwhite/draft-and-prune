from z3 import *

# Student indices: Louis=0, Mollie=1, Onyx=2, Ryan=3, Tiffany=4, Yoshio=5
students = ["Louis", "Mollie", "Onyx", "Ryan", "Tiffany", "Yoshio"]

# Year assignment variables: year[i] = student assigned to 1921+i
year = [Int(f"year_{i}") for i in range(4)]

# Base solver
solver = Solver()

# Domain constraints: each year assigned a student index 0-5
for i in range(4):
    solver.add(And(year[i] >= 0, year[i] <= 5))

# Distinctness constraint: all four years assigned to different students
solver.add(Distinct(year))

# Only Louis or Tiffany can be assigned to 1923 (year index 2)
solver.add(Or(year[2] == 0, year[2] == 4))

# Mollie constraint: if Mollie is assigned, she must be in year 0 or 1
# This means: if any year[i] == 1, then i must be 0 or 1
for i in range(4):
    solver.add(Implies(year[i] == 1, Or(i == 0, i == 1)))

# Tiffany–Ryan dependency: if Tiffany is assigned, then Ryan must be assigned
# This means: if any year[i] == 4, then there exists j such that year[j] == 3
tiffany_assigned = Or(*[year[i] == 4 for i in range(4)])
ryan_assigned = Or(*[year[i] == 3 for i in range(4)])
solver.add(Implies(tiffany_assigned, ryan_assigned))

# Ryan–Onyx adjacency: if Ryan is assigned, then Onyx must be assigned to the year immediately prior
# This means: if Ryan is in position i (0-indexed), then Onyx must be in position i-1
# We'll encode this as: for each possible Ryan position i>0, if year[i]==3 then year[i-1]==2
# For i=0 (1921), Ryan cannot be there because no prior year exists
for i in range(1, 4):
    solver.add(Implies(year[i] == 3, year[i-1] == 2))

# Given condition: both Ryan and Yoshio are assigned
solver.add(ryan_assigned)
yoshio_assigned = Or(*[year[i] == 5 for i in range(4)])
solver.add(yoshio_assigned)

# Answer choices (indices 0-4)
choices = [
    ("Louis is assigned to 1923.", year[2] == 0),
    ("Mollie is assigned to 1921.", year[0] == 1),
    ("Onyx is assigned to 1922.", year[1] == 2),
    ("Tiffany is assigned to 1924.", year[3] == 4),
    ("Yoshio is assigned to 1922.", year[1] == 5)
]

# Check each choice
answer_index_list = []
for idx, (desc, condition) in enumerate(choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(condition)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

# Output the index of the correct choice (first satisfiable one as per LSAT format)
print(answer_index_list[0] if answer_index_list else -1)