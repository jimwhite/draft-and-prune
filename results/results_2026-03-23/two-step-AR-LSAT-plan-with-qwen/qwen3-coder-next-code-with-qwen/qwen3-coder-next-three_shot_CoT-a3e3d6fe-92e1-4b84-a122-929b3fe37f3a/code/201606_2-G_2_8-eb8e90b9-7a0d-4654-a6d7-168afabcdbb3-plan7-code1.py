from z3 import *

# Student indices: Louis=0, Mollie=1, Onyx=2, Ryan=3, Tiffany=4, Yoshio=5
# Year indices: 1921=0, 1922=1, 1923=2, 1924=3

# pos[y] = student index assigned to year y (0-5)
pos = [Int(f"pos_{y}") for y in range(4)]

# Base solver
solver = Solver()

# Domain constraints: each pos[y] must be in 0..5
for y in range(4):
    solver.add(pos[y] >= 0, pos[y] <= 5)

# All assigned students are distinct
solver.add(Distinct(pos))

# Ryan (3) and Yoshio (5) must be assigned (appear in pos)
solver.add(Or(*[pos[y] == 3 for y in range(4)]))
solver.add(Or(*[pos[y] == 5 for y in range(4)]))

# Only Louis (0) or Tiffany (4) can be assigned to 1923 (year index 2)
solver.add(Or(pos[2] == 0, pos[2] == 4))

# Mollie conditional: if Mollie (1) is assigned, she must be in 1921 or 1922
# This is equivalent to: if pos[y] == 1, then y in {0,1}
for y in range(4):
    solver.add(Implies(pos[y] == 1, Or(y == 0, y == 1)))

# Ryan-Onyx conditional: if Ryan (3) is assigned, then Onyx (2) must be in the year immediately before
# Since Ryan is assigned (we assume), we need: if pos[yr] = 3, then yr > 0 and pos[yr-1] = 2
# We'll encode this by adding constraints that enforce the relationship when Ryan is assigned:
for y in range(4):
    # If Ryan is at year y, then Onyx must be at year y-1
    solver.add(Implies(pos[y] == 3, And(y > 0, pos[y-1] == 2)))

# Answer choices (as conditions to check for SAT)
answer_choices = [
    ("Louis is assigned to 1923.", pos[2] == 0),           # A
    ("Mollie is assigned to 1921.", pos[0] == 1),          # B
    ("Onyx is assigned to 1922.", pos[1] == 2),            # C
    ("Tiffany is assigned to 1924.", pos[3] == 4),         # D
    ("Yoshio is assigned to 1922.", pos[1] == 5)           # E
]

# Check each choice
answer_index_list = []
for idx, (desc, condition) in enumerate(answer_choices):
    s_chk = Solver()
    # Add all base constraints
    for a in solver.assertions():
        s_chk.add(a)
    
    # Add the specific condition for this choice
    s_chk.add(condition)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

# Print the index of the choice that could be true
print(answer_index_list[0] if answer_index_list else -1)