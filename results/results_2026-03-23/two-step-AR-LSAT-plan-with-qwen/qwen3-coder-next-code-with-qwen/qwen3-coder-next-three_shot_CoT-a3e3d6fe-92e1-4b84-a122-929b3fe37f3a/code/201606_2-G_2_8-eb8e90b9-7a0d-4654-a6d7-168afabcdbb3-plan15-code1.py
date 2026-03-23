from z3 import *

# Student indices: Louis=0, Mollie=1, Onyx=2, Ryan=3, Tiffany=4, Yoshio=5
# Year indices: 1921=0, 1922=1, 1923=2, 1924=3

# Boolean variables: x[s][y] = True if student s is assigned to year y
x = [[Bool(f"x_{s}_{y}") for y in range(4)] for s in range(6)]

solver = Solver()

# Each year has exactly one student assigned
for y in range(4):
    solver.add(Sum([If(x[s][y], 1, 0) for s in range(6)]) == 1)

# Each student is assigned to at most one year
for s in range(6):
    solver.add(Sum([If(x[s][y], 1, 0) for y in range(4)]) <= 1)

# Exactly four students are assigned (since exactly four years)
solver.add(Sum([Sum([If(x[s][y], 1, 0) for y in range(4)]) > 0 for s in range(6)]) == 4)

# Premise: Ryan and Yoshio are assigned
solver.add(Sum([If(x[3][y], 1, 0) for y in range(4)]) == 1)
solver.add(Sum([If(x[5][y], 1, 0) for y in range(4)]) == 1)

# Only Louis or Tiffany can be assigned to 1923 (year index 2)
for s in range(6):
    if s != 0 and s != 4:  # not Louis (0) or Tiffany (4)
        solver.add(Not(x[s][2]))

# Mollie constraint: if assigned, must be in 1921 or 1922
# This means Mollie cannot be assigned to 1923 or 1924
solver.add(Not(x[1][2]))
solver.add(Not(x[1][3]))

# Ryan-Onyx constraint: if Ryan is assigned to year y, then Onyx must be assigned to year y-1
# Since Ryan is assigned (premise), enforce for each possible year:
for y in range(4):
    if y == 0:  # Ryan cannot be assigned to 1921 (no prior year)
        solver.add(Not(x[3][0]))
    else:
        # x[3][y] implies x[2][y-1]
        solver.add(Or(Not(x[3][y]), x[2][y-1]))

# Answer choices (check which could be true under the premise)
answer_choices = [
    ("Louis is assigned to 1923.", x[0][2]),      # A
    ("Mollie is assigned to 1921.", x[1][0]),     # B
    ("Onyx is assigned to 1922.", x[2][1]),       # C
    ("Tiffany is assigned to 1924.", x[4][3]),    # D
    ("Yoshio is assigned to 1922.", x[5][1])      # E
]

answer_index_list = []
for idx, (desc, constraint) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(constraint)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)