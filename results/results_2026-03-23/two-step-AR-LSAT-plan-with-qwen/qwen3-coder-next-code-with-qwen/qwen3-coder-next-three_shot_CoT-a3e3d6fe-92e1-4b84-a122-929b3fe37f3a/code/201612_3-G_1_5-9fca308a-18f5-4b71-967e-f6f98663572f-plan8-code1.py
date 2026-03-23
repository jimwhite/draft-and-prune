from z3 import *

# Student indices: Juana=0, Kelly=1, Lateefah=2, Mei=3, Olga=4
students = ["Juana", "Kelly", "Lateefah", "Mei", "Olga"]
n = 5

# Boolean variables for team assignment: green[i] = True if student i is on green team
green = [Bool(f"green_{i}") for i in range(n)]

# Boolean variables for facilitator assignment: facilitator[i] = True if student i is a facilitator
facilitator = [Bool(f"facilitator_{i}") for i in range(n)]

# Base solver
solver = Solver()

# Team-size constraints: exactly 2 on one team, 3 on the other
solver.add(Or(Sum([If(green[i], 1, 0) for i in range(n)]) == 2,
              Sum([If(green[i], 1, 0) for i in range(n)]) == 3))

# Exactly one facilitator per team
solver.add(Sum([If(And(green[i], facilitator[i]), 1, 0) for i in range(n)]) == 1)
solver.add(Sum([If(And(Not(green[i]), facilitator[i]), 1, 0) for i in range(n)]) == 1)

# Fixed constraints
solver.add(green[2] == True)  # Lateefah is on green team
solver.add(facilitator[4] == True)  # Olga is a facilitator
solver.add(facilitator[1] == False)  # Kelly is not a facilitator
solver.add(green[0] != green[4])  # Juana and Olga on different teams

# Assumption: Mei is on green team
solver.add(green[3] == True)

# Answer choices (as logical conditions)
answer_conditions = [
    green[0],  # Juana is assigned to the green team
    Not(green[1]),  # Kelly is assigned to the red team (i.e., not on green)
    green[4],  # Olga is assigned to the green team
    facilitator[2],  # Lateefah is a facilitator
    facilitator[3]   # Mei is a facilitator
]

# Check each answer choice using proof by contradiction
answer_index_list = []
for idx, cond in enumerate(answer_conditions):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add negation of the condition
    s_chk.add(Not(cond))
    
    # If UNSAT, this condition must be true
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)