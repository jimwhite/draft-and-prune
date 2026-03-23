from z3 import *

# Student indices: Louis=0, Mollie=1, Onyx=2, Ryan=3, Tiffany=4, Yoshio=5
students = ["Louis", "Mollie", "Onyx", "Ryan", "Tiffany", "Yoshio"]
year_indices = {1921: 0, 1922: 1, 1923: 2, 1924: 3}

# Create year assignment variables for each student (-1 means unassigned)
year = [Int(f"year_{i}") for i in range(6)]

# Create boolean variables to indicate if a student is assigned
assigned = [Bool(f"assigned_{i}") for i in range(6)]

# Base solver
solver = Solver()

# Domain constraints: assigned students get years 1921-1924, unassigned get -1
for i in range(6):
    solver.add(Implies(assigned[i], Or(year[i] == 1921, year[i] == 1922, year[i] == 1923, year[i] == 1924)))
    solver.add(Implies(Not(assigned[i]), year[i] == -1))

# Exactly four students are assigned
solver.add(Sum([If(assigned[i], 1, 0) for i in range(6)]) == 4)

# The four assigned students must cover all years 1921-1924 exactly once
# Enforce distinctness of assigned years
non_assigned_years = [year[i] for i in range(6)]
solver.add(Distinct(*[If(assigned[i], year[i], 0) for i in range(6)]))

# Also ensure all four years are covered by assigned students
for y in [1921, 1922, 1923, 1924]:
    solver.add(Or(*[And(assigned[i], year[i] == y) for i in range(6)]))

# Fixed scenario: Ryan and Yoshio are assigned (year != -1)
solver.add(assigned[3] == True)  # Ryan
solver.add(assigned[5] == True)  # Yoshio

# Only Louis or Tiffany can be assigned to 1923
for i in [0, 4]:  # Louis and Tiffany can be assigned to 1923
    solver.add(Implies(And(assigned[i], year[i] == 1923), True))
for i in [1, 2, 5]:  # Mollie, Onyx, Yoshio cannot be assigned to 1923
    solver.add(Implies(year[i] == 1923, Not(assigned[i])))

# If Mollie is assigned, she must be in 1921 or 1922
solver.add(Implies(assigned[1], Or(year[1] == 1921, year[1] == 1922)))

# If Tiffany is assigned, then Ryan must be assigned (already satisfied by scenario)
solver.add(Implies(assigned[4], assigned[3]))

# If Ryan is assigned, Onyx must be assigned to the year immediately prior
solver.add(Implies(assigned[3], And(
    assigned[2],
    year[2] == year[3] - 1
)))

# Answer choices (as conditions to check for possibility under the scenario)
answer_conditions = [
    year[0] == 1923,  # Louis is assigned to 1923
    year[1] == 1921,  # Mollie is assigned to 1921
    year[2] == 1922,  # Onyx is assigned to 1922
    year[4] == 1924,  # Tiffany is assigned to 1924
    year[5] == 1922   # Yoshio is assigned to 1922
]

# Check each answer choice
answer_index_list = []
for idx, cond in enumerate(answer_conditions):
    s_chk = Solver()
    for a in solver.assertions():
        s_chk.add(a)
    s_chk.add(cond)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)