from z3 import *

# Student indices: Louis, Mollie, Onyx, Ryan, Tiffany, Yoshio
(L, M, O, R, T, Y) = range(6)

# Year indices: 0->1921, 1->1922, 2->1923, 3->1924
# assign[s] = year index if assigned, -1 if not assigned
assign = [Int(f"assign_{i}") for i in range(6)]

# Base solver
solver = Solver()

# Domain constraints: each assigned student gets a year in [0,3], unassigned get -1
for i in range(6):
    solver.add(Or(assign[i] == -1, And(assign[i] >= 0, assign[i] <= 3)))

# Exactly four students assigned
solver.add(Sum([If(assign[i] != -1, 1, 0) for i in range(6)]) == 4)

# Year uniqueness: assigned students get distinct years
year_vars = [assign[i] for i in range(6)]
solver.add(Implies(And(assign[0] != -1, assign[1] != -1), assign[0] != assign[1]))
solver.add(Implies(And(assign[0] != -1, assign[2] != -1), assign[0] != assign[2]))
solver.add(Implies(And(assign[0] != -1, assign[3] != -1), assign[0] != assign[3]))
solver.add(Implies(And(assign[0] != -1, assign[4] != -1), assign[0] != assign[4]))
solver.add(Implies(And(assign[0] != -1, assign[5] != -1), assign[0] != assign[5]))
solver.add(Implies(And(assign[1] != -1, assign[2] != -1), assign[1] != assign[2]))
solver.add(Implies(And(assign[1] != -1, assign[3] != -1), assign[1] != assign[3]))
solver.add(Implies(And(assign[1] != -1, assign[4] != -1), assign[1] != assign[4]))
solver.add(Implies(And(assign[1] != -1, assign[5] != -1), assign[1] != assign[5]))
solver.add(Implies(And(assign[2] != -1, assign[3] != -1), assign[2] != assign[3]))
solver.add(Implies(And(assign[2] != -1, assign[4] != -1), assign[2] != assign[4]))
solver.add(Implies(And(assign[2] != -1, assign[5] != -1), assign[2] != assign[5]))
solver.add(Implies(And(assign[3] != -1, assign[4] != -1), assign[3] != assign[4]))
solver.add(Implies(And(assign[3] != -1, assign[5] != -1), assign[3] != assign[5]))
solver.add(Implies(And(assign[4] != -1, assign[5] != -1), assign[4] != assign[5]))

# 1923 constraint: only Louis or Tiffany can be assigned to 1923
for i in range(6):
    if i != L and i != T:
        solver.add(assign[i] != 2)

# Mollie constraint: if assigned, must be in 1921 or 1922
solver.add(Implies(assign[M] != -1, Or(assign[M] == 0, assign[M] == 1)))

# Tiffany ⇒ Ryan constraint: if Tiffany assigned, then Ryan must be assigned
solver.add(Implies(assign[T] != -1, assign[R] != -1))

# Ryan ⇒ Onyx prior constraint: if Ryan assigned, then Onyx must be assigned and immediately before
solver.add(Implies(assign[R] != -1, And(
    assign[O] != -1,
    assign[O] == assign[R] - 1
)))

# Given assumption: Ryan and Yoshio are both assigned
solver.add(assign[R] != -1, assign[Y] != -1)

# Answer choices indices: A=0 (Louis to 1923), B=1 (Mollie to 1921), C=2 (Onyx to 1922), D=3 (Tiffany to 1924), E=4 (Yoshio to 1922)
answer_index_list = []

# Check each choice
# A: Louis assigned to 1923 (year index 2)
s_chk = Solver()
s_chk.add(solver.assertions())
s_chk.add(assign[L] == 2)
if s_chk.check() == sat:
    answer_index_list.append(0)

# B: Mollie assigned to 1921 (year index 0)
s_chk = Solver()
s_chk.add(solver.assertions())
s_chk.add(assign[M] == 0)
if s_chk.check() == sat:
    answer_index_list.append(1)

# C: Onyx assigned to 1922 (year index 1)
s_chk = Solver()
s_chk.add(solver.assertions())
s_chk.add(assign[O] == 1)
if s_chk.check() == sat:
    answer_index_list.append(2)

# D: Tiffany assigned to 1924 (year index 3)
s_chk = Solver()
s_chk.add(solver.assertions())
s_chk.add(assign[T] == 3)
if s_chk.check() == sat:
    answer_index_list.append(3)

# E: Yoshio assigned to 1922 (year index 1)
s_chk = Solver()
s_chk.add(solver.assertions())
s_chk.add(assign[Y] == 1)
if s_chk.check() == sat:
    answer_index_list.append(4)

print(answer_index_list)