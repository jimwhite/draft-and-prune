from z3 import *

# Student indices: Juana=0, Kelly=1, Lateefah=2, Mei=3, Olga=4
students = ["Juana", "Kelly", "Lateefah", "Mei", "Olga"]

# Boolean variables for team assignments: green[i] = True if student i is on green team
green = [Bool(f"green_{i}") for i in range(5)]

# Boolean variables for facilitator assignments
facilitator = [Bool(f"facilitator_{i}") for i in range(5)]

# Base solver
solver = Solver()

# Team-size constraint: one team has 2 members, the other has 3
green_count = Sum([If(green[i], 1, 0) for i in range(5)])
solver.add(Or(green_count == 2, green_count == 3))

# Lateefah is on green team
solver.add(green[2] == True)

# Juana and Olga are on different teams
solver.add(green[0] != green[4])

# Exactly two facilitators (one per team)
solver.add(Sum([If(facilitator[i], 1, 0) for i in range(5)]) == 2)

# One facilitator per team
# For green team: exactly one facilitator among those on green
green_facilitators = [If(And(green[i], facilitator[i]), 1, 0) for i in range(5)]
solver.add(Sum(green_facilitators) == 1)

# For red team: exactly one facilitator among those not on green
red_facilitators = [If(And(Not(green[i]), facilitator[i]), 1, 0) for i in range(5)]
solver.add(Sum(red_facilitators) == 1)

# Kelly is not a facilitator
solver.add(facilitator[1] == False)

# Olga is a facilitator (given)
solver.add(facilitator[4] == True)

# Mei is on green team (premise of the conditional)
solver.add(green[3] == True)

# Answer choices: 
# 0: Juana is assigned to the green team (green[0] == True)
# 1: Kelly is assigned to the red team (Not(green[1]) == True)
# 2: Olga is assigned to the green team (green[4] == True)
# 3: Lateefah is a facilitator (facilitator[2] == True)
# 4: Mei is a facilitator (facilitator[3] == True)

answer_choices = [
    green[0],           # Juana on green
    Not(green[1]),      # Kelly on red
    green[4],           # Olga on green
    facilitator[2],     # Lateefah is facilitator
    facilitator[3]      # Mei is facilitator
]

# Check each answer choice using proof by contradiction
answer_index_list = []
for idx, cond in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add the negation of the condition (assume it's NOT true)
    s_chk.add(Not(cond))
    
    # If UNSAT, then the condition must be true
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)