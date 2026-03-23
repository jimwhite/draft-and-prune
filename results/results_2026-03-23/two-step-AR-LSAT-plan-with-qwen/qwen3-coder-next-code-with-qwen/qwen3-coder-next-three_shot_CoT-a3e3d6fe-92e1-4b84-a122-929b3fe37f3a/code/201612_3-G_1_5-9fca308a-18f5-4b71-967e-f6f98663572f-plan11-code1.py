from z3 import *

# Student indices: Juana=0, Kelly=1, Lateefah=2, Mei=3, Olga=4
green = [Bool(f"green_{i}") for i in range(5)]
facilitator = [Bool(f"facilitator_{i}") for i in range(5)]

solver = Solver()

# Team size constraints: one team has 2 members, the other has 3
green_count = Sum([If(green[i], 1, 0) for i in range(5)])
solver.add(Or(green_count == 2, green_count == 3))

# Each team has exactly one facilitator
solver.add(Sum([If(And(green[i], facilitator[i]), 1, 0) for i in range(5)]) == 1)
solver.add(Sum([If(And(Not(green[i]), facilitator[i]), 1, 0) for i in range(5)]) == 1)

# Fixed assignment constraints
solver.add(green[2] == True)  # Lateefah is on green team
solver.add(green[0] != green[4])  # Juana and Olga on different teams
solver.add(facilitator[4] == True)  # Olga is a facilitator
solver.add(facilitator[1] == False)  # Kelly is not a facilitator

# Hypothetical: Mei is on green team
solver.add(green[3] == True)

# Answer choices (as logical conditions)
choices = [
    green[0] == True,           # Juana is on green team
    green[1] == False,          # Kelly is on red team
    green[4] == True,           # Olga is on green team
    facilitator[2] == True,     # Lateefah is a facilitator
    facilitator[3] == True      # Mei is a facilitator
]

# Check each choice by asserting its negation and checking UNSAT
answer_index_list = []
for idx, cond in enumerate(choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(Not(cond))
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)