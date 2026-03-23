from z3 import *

# Student indices: Louis=0, Mollie=1, Onyx=2, Ryan=3, Tiffany=4, Yoshio=5
students = ["Louis", "Mollie", "Onyx", "Ryan", "Tiffany", "Yoshio"]
n_students = 6

# Year indices: 1921=0, 1922=1, 1923=2, 1924=3
n_years = 4

# Assignment variables: year[i] is the year assigned to student i (-1 if unassigned)
year = [Int(f"year_{i}") for i in range(n_students)]

# Assignment selectors: assign[i] == 1 if student i is assigned, 0 otherwise
assign = [Int(f"assign_{i}") for i in range(n_students)]

# Base solver
solver = Solver()

# Domain constraints for year variables
for i in range(n_students):
    solver.add(Or(year[i] == -1, And(year[i] >= 0, year[i] <= n_years-1)))

# Domain constraints for assign variables (binary)
for i in range(n_students):
    solver.add(Or(assign[i] == 0, assign[i] == 1))

# Link assign and year: assign[i] == 1 iff year[i] != -1
for i in range(n_students):
    solver.add(Implies(assign[i] == 1, year[i] != -1))
    solver.add(Implies(year[i] != -1, assign[i] == 1))

# Exactly four students assigned
solver.add(Sum(assign) == 4)

# All assigned students get distinct years
for i in range(n_students):
    for j in range(i+1, n_students):
        solver.add(Implies(And(assign[i] == 1, assign[j] == 1), year[i] != year[j]))

# Only Louis (0) or Tiffany (4) can be assigned to 1923 (year index 2)
for i in range(n_students):
    if i != 0 and i != 4:
        solver.add(Implies(assign[i] == 1, year[i] != 2))

# Mollie constraint: if assigned, must be in 1921 or 1922 (year indices 0 or 1)
solver.add(Implies(assign[1] == 1, Or(year[1] == 0, year[1] == 1)))

# Tiffany → Ryan constraint: if Tiffany assigned, then Ryan must be assigned
solver.add(Implies(assign[4] == 1, assign[3] == 1))

# Ryan → Onyx-before constraint: if Ryan assigned, then:
# - Onyx must be assigned
# - Onyx's year = Ryan's year - 1
# - Ryan cannot be in 1921 (year index 0)
solver.add(Implies(assign[3] == 1, assign[2] == 1))
solver.add(Implies(assign[3] == 1, year[2] == year[3] - 1))
solver.add(Implies(assign[3] == 1, year[3] != 0))

# Given condition: Ryan and Yoshio are assigned
solver.add(assign[3] == 1)
solver.add(assign[5] == 1)

# Answer choices (indices: A=0, B=1, C=2, D=3, E=4)
# A: Louis assigned to 1923 → assign[0] == 1 ∧ year[0] == 2
# B: Mollie assigned to 1921 → assign[1] == 1 ∧ year[1] == 0
# C: Onyx assigned to 1922 → assign[2] == 1 ∧ year[2] == 1
# D: Tiffany assigned to 1924 → assign[4] == 1 ∧ year[4] == 3
# E: Yoshio assigned to 1922 → assign[5] == 1 ∧ year[5] == 1

answer_index_list = []

# Check each answer choice
for idx, condition in enumerate([
    And(assign[0] == 1, year[0] == 2),
    And(assign[1] == 1, year[1] == 0),
    And(assign[2] == 1, year[2] == 1),
    And(assign[4] == 1, year[4] == 3),
    And(assign[5] == 1, year[5] == 1)
]):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(condition)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)