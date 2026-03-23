from z3 import *

# Student indices: Louis=0, Mollie=1, Onyx=2, Ryan=3, Tiffany=4, Yoshio=5
# Year indices: 0=1921, 1=1922, 2=1923, 3=1924

s = [[Bool(f"s_{i}_{j}") for j in range(4)] for i in range(6)]

solver = Solver()

# Each student assigned to at most one year
for i in range(6):
    solver.add(Sum([If(s[i][j], 1, 0) for j in range(4)]) <= 1)

# Each year assigned to exactly one student
for j in range(4):
    solver.add(Sum([If(s[i][j], 1, 0) for i in range(6)]) == 1)

# Only Louis or Tiffany can be assigned to 1923 (year index 2)
for i in range(6):
    if i != 0 and i != 4:
        solver.add(Not(s[i][2]))
# Also ensure at least one of Louis or Tiffany is assigned to 1923
solver.add(Or(s[0][2], s[4][2]))

# Mollie must be assigned to 1921 or 1922 if assigned
solver.add(Not(s[1][2]))
solver.add(Not(s[1][3]))

# Tiffany ⇒ Ryan: if Tiffany is assigned, then Ryan must be assigned
tiffany_assigned = Or([s[4][j] for j in range(4)])
ryan_assigned = Or([s[3][j] for j in range(4)])
solver.add(Implies(tiffany_assigned, ryan_assigned))

# Ryan ⇒ Onyx immediately prior
# Ryan cannot be in 1921 (year index 0)
solver.add(Not(s[3][0]))
# For years 1922, 1923, 1924 (indices 1,2,3): if Ryan is in year j, Onyx must be in year j-1
for j in range(1, 4):
    solver.add(Implies(s[3][j], s[2][j-1]))

# Given condition: both Ryan and Yoshio are assigned
solver.add(Or([s[3][j] for j in range(4)]))
solver.add(Or([s[5][j] for j in range(4)]))

# Answer choices
choices = [
    s[0][2],  # Louis is assigned to 1923
    s[1][0],  # Mollie is assigned to 1921
    s[2][1],  # Onyx is assigned to 1922
    s[4][3],  # Tiffany is assigned to 1924
    s[5][1]   # Yoshio is assigned to 1922
]

answer_index_list = []
for idx, cond in enumerate(choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(cond)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)