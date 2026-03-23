from z3 import *

# Student indices: Louis=0, Mollie=1, Onyx=2, Ryan=3, Tiffany=4, Yoshio=5
students = ["Louis", "Mollie", "Onyx", "Ryan", "Tiffany", "Yoshio"]
student_idx = {s: i for i, s in enumerate(students)}

# Years: 1921=0, 1922=1, 1923=2, 1924=3
years = [0, 1, 2, 3]
year_names = {0: "1921", 1: "1922", 2: "1923", 3: "1924"}

# Assignment variables: assigned[i][y] = True if student i is assigned to year y
assigned = [[Bool(f"assigned_{students[i]}_{year_names[y]}") for y in years] for i in range(6)]

# Base solver
solver = Solver()

# Each year is assigned exactly one student
for y in years:
    solver.add(Sum([If(assigned[i][y], 1, 0) for i in range(6)]) == 1)

# Each assigned student is assigned to exactly one year
for i in range(6):
    solver.add(Sum([If(assigned[i][y], 1, 0) for y in years]) <= 1)

# Exactly four students are assigned (since there are four years)
solver.add(Sum([Sum([If(assigned[i][y], 1, 0) for y in years]) for i in range(6)]) == 4)

# Premise: Ryan and Yoshio are both assigned
solver.add(Sum([If(assigned[student_idx["Ryan"]][y], 1, 0) for y in years]) == 1)
solver.add(Sum([If(assigned[student_idx["Yoshio"]][y], 1, 0) for y in years]) == 1)

# Only Louis or Tiffany can be assigned to 1923
solver.add(Or(assigned[student_idx["Louis"]][2], assigned[student_idx["Tiffany"]][2]))
for i in range(6):
    if students[i] not in ["Louis", "Tiffany"]:
        solver.add(Not(assigned[i][2]))

# If Mollie is assigned, she must be in 1921 or 1922
solver.add(Implies(
    Sum([If(assigned[student_idx["Mollie"]][y], 1, 0) for y in years]) == 1,
    Or(assigned[student_idx["Mollie"]][0], assigned[student_idx["Mollie"]][1])
))

# If Tiffany is assigned, then Ryan must be assigned (already satisfied by premise)
solver.add(Implies(
    Sum([If(assigned[student_idx["Tiffany"]][y], 1, 0) for y in years]) == 1,
    Sum([If(assigned[student_idx["Ryan"]][y], 1, 0) for y in years]) == 1
))

# If Ryan is assigned to year Y, then Onyx must be assigned to Y-1
# For 1922 (index 1): Ryan in 1922 → Onyx in 1921
solver.add(Implies(assigned[student_idx["Ryan"]][1], assigned[student_idx["Onyx"]][0]))
# For 1923 (index 2): Ryan in 1923 → Onyx in 1922
solver.add(Implies(assigned[student_idx["Ryan"]][2], assigned[student_idx["Onyx"]][1]))
# For 1924 (index 3): Ryan in 1924 → Onyx in 1923
solver.add(Implies(assigned[student_idx["Ryan"]][3], assigned[student_idx["Onyx"]][2]))
# Ryan cannot be in 1921 (no predecessor)
solver.add(Not(assigned[student_idx["Ryan"]][0]))

# Answer choices
answer_choices = [
    assigned[student_idx["Louis"]][2],  # Louis is assigned to 1923
    assigned[student_idx["Mollie"]][0], # Mollie is assigned to 1921
    assigned[student_idx["Onyx"]][1],   # Onyx is assigned to 1922
    assigned[student_idx["Tiffany"]][3],# Tiffany is assigned to 1924
    assigned[student_idx["Yoshio"]][1]  # Yoshio is assigned to 1922
]

# Check each answer choice
answer_index_list = []
for idx, cond in enumerate(answer_choices):
    s_chk = Solver()
    # Add all base constraints and premise
    for a in solver.assertions():
        s_chk.add(a)
    # Add the answer choice condition
    s_chk.add(cond)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)