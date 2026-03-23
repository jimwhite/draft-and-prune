from z3 import *

# Student indices: Juana=0, Kelly=1, Lateefah=2, Mei=3, Olga=4
students = ["Juana", "Kelly", "Lateefah", "Mei", "Olga"]
n = 5

# Team assignment variables: is_green[i] means student i is on green team
is_green = [Bool(f"is_green_{i}") for i in range(n)]

# Facilitator variables: green_fac[i] means student i is facilitator of green team
green_fac = [Bool(f"green_fac_{i}") for i in range(n)]
red_fac = [Bool(f"red_fac_{i}") for i in range(n)]

# Base solver
solver = Solver()

# Each student is on exactly one team (green or red)
for i in range(n):
    solver.add(is_green[i] != Not(is_green[i]))  # tautology, but we'll enforce explicitly
    solver.add(Or(is_green[i], Not(is_green[i])))  # tautology, but we'll add proper constraint
    solver.add(Or(is_green[i], Not(is_green[i])))  # redundant, but we'll add proper constraint

# Proper team assignment: each student is on exactly one team
for i in range(n):
    solver.add(Xor(is_green[i], Not(is_green[i])))  # This is always true, so we need to be explicit
    # Instead: enforce that if not green then red (implicitly)
    # Better: just use is_green[i] as the variable, and red team is implicit

# Actually, let's simplify: use only is_green[i], and red team is !is_green[i]
# So each student is on exactly one team by construction

# Team size constraint: one team has 2, the other has 3
solver.add(Sum([If(is_green[i], 1, 0) for i in range(n)]) == 2)
solver.add(Sum([If(is_green[i], 1, 0) for i in range(n)]) == 3)
# But we need exactly one of these to hold. Since they're mutually exclusive, use Or:
solver.add(Or(Sum([If(is_green[i], 1, 0) for i in range(n)]) == 2,
              Sum([If(is_green[i], 1, 0) for i in range(n)]) == 3))

# Fixed constraints
# Juana ≠ Olga (different teams)
solver.add(is_green[0] != is_green[4])

# Lateefah ∈ green
solver.add(is_green[2] == True)

# Olga is a facilitator: either green_fac[4] or red_fac[4]
solver.add(Or(green_fac[4], red_fac[4]))

# Facilitator membership constraints
for i in range(n):
    # green facilitator must be on green team
    solver.add(Implies(green_fac[i], is_green[i]))
    # red facilitator must be on red team (i.e., not green)
    solver.add(Implies(red_fac[i], Not(is_green[i])))

# Exactly one facilitator per team
solver.add(Sum([If(green_fac[i], 1, 0) for i in range(n)]) == 1)
solver.add(Sum([If(red_fac[i], 1, 0) for i in range(n)]) == 1)

# Kelly is not a facilitator
solver.add(Not(green_fac[1]), Not(red_fac[1]))

# Hypothetical condition: Mei is assigned to green team
solver.add(is_green[3] == True)

# Answer choices (indices 0-4)
# A: Juana is assigned to the green team. -> is_green[0]
# B: Kelly is assigned to the red team. -> Not(is_green[1])
# C: Olga is assigned to the green team. -> is_green[4]
# D: Lateefah is a facilitator. -> green_fac[2]
# E: Mei is a facilitator. -> green_fac[3]

answer_choices = [
    ("Juana is assigned to the green team.", lambda: is_green[0]),
    ("Kelly is assigned to the red team.", lambda: Not(is_green[1])),
    ("Olga is assigned to the green team.", lambda: is_green[4]),
    ("Lateefah is a facilitator.", lambda: green_fac[2]),
    ("Mei is a facilitator.", lambda: green_fac[3])
]

answer_index_list = []
for idx, (desc, condition) in enumerate(answer_choices):
    s_chk = Solver()
    # Add all base constraints + Mei on green (already added to solver)
    s_chk.add(solver.assertions())
    
    # Add the negation of the condition (to test if it must be true)
    s_chk.add(Not(condition()))
    
    # If UNSAT, then the condition must be true
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)