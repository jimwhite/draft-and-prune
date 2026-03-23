from z3 import *

# Student indices: Juana=0, Kelly=1, Lateefah=2, Mei=3, Olga=4
students = ["Juana", "Kelly", "Lateefah", "Mei", "Olga"]

# Team assignment variables: green[i] = True if student i is on green team
green = [Bool(f"green_{i}") for i in range(5)]

# Facilitator variables: fac[i] = True if student i is a facilitator
fac = [Bool(f"fac_{i}") for i in range(5)]

# Base solver
solver = Solver()

# Team size constraint: one team has 2 members, the other has 3
g_sum = Sum([If(green[i], 1, 0) for i in range(5)])
solver.add(Or(g_sum == 2, g_sum == 3))

# Fixed constraints
# Lateefah is on green team
solver.add(green[2] == True)
# Juana and Olga are on different teams
solver.add(green[0] != green[4])
# Kelly is not a facilitator
solver.add(fac[1] == False)
# Olga is a facilitator
solver.add(fac[4] == True)

# Exactly one facilitator per team
# For green team: if g_sum = 2, then exactly 1 facilitator among green members
# If g_sum = 3, then exactly 1 facilitator among green members
solver.add(Implies(g_sum == 2, Sum([If(And(green[i], fac[i]), 1, 0) for i in range(5)]) == 1))
solver.add(Implies(g_sum == 3, Sum([If(And(green[i], fac[i]), 1, 0) for i in range(5)]) == 1))

# For red team: exactly one facilitator among non-green members
solver.add(Implies(g_sum == 2, Sum([If(And(Not(green[i]), fac[i]), 1, 0) for i in range(5)]) == 1))
solver.add(Implies(g_sum == 3, Sum([If(And(Not(green[i]), fac[i]), 1, 0) for i in range(5)]) == 1))

# Premise: Mei is on green team
solver.add(green[3] == True)

# Answer choices (as logical statements)
answer_choices = [
    green[0],  # Juana is assigned to the green team
    Not(green[1]),  # Kelly is assigned to the red team (i.e., not on green)
    green[4],  # Olga is assigned to the green team
    fac[2],  # Lateefah is a facilitator
    fac[3]   # Mei is a facilitator
]

# Check each answer choice by proving necessity (negation leads to UNSAT)
answer_index_list = []
for idx, stmt in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert the negation of the statement
    s_chk.add(Not(stmt))
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)