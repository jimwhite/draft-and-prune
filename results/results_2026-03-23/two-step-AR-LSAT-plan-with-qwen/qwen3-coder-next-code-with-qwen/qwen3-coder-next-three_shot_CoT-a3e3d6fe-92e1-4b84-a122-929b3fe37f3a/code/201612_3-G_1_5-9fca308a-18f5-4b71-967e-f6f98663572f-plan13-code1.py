from z3 import *

# Student indices: Juana=0, Kelly=1, Lateefah=2, Mei=3, Olga=4
students = ["Juana", "Kelly", "Lateefah", "Mei", "Olga"]

# Boolean variables for team assignment: True = green, False = red
team = [Bool(f"team_{i}") for i in range(5)]

# Boolean variables for facilitator status
fac = [Bool(f"fac_{i}") for i in range(5)]

# Base solver
solver = Solver()

# Team-size constraints: one team has 2 members, the other has 3
# Since Lateefah is on green (team[2] == True), we consider both possibilities
# But the problem states "one team will have two members, and the other will have three"
# So total green team size is either 2 or 3
green_count = Sum([If(team[i], 1, 0) for i in range(5)])
solver.add(Or(green_count == 2, green_count == 3))

# Lateefah is assigned to the green team
solver.add(team[2] == True)

# Exactly one facilitator per team
# For green team: if a student is on green, they can be facilitator; otherwise not
# For red team: if a student is on red, they can be facilitator; otherwise not
# We need exactly one facilitator for green and one for red

# Green facilitator constraint: exactly one student on green is a facilitator
green_facilitator = [And(team[i], fac[i]) for i in range(5)]
solver.add(Sum([If(green_facilitator[i], 1, 0) for i in range(5)]) == 1)

# Red facilitator constraint: exactly one student on red is a facilitator
red_facilitator = [And(Not(team[i]), fac[i]) for i in range(5)]
solver.add(Sum([If(red_facilitator[i], 1, 0) for i in range(5)]) == 1)

# Given constraints
# Juana is assigned to a different team than Olga
solver.add(team[0] != team[4])

# Kelly is not a facilitator
solver.add(fac[1] == False)

# Olga is a facilitator
solver.add(fac[4] == True)

# Hypothesis: Mei is assigned to the green team
solver.add(team[3] == True)

# Answer choices (indices correspond to positions in the list)
answer_choices = [
    "Juana is assigned to the green team.",  # team[0] == True
    "Kelly is assigned to the red team.",    # team[1] == False
    "Olga is assigned to the green team.",   # team[4] == True
    "Lateefah is a facilitator.",            # fac[2] == True
    "Mei is a facilitator."                  # fac[3] == True
]

# Check each answer choice for necessity
answer_index_list = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Negate the choice condition
    if idx == 0:  # Juana is assigned to green team
        s_chk.add(team[0] != True)
    elif idx == 1:  # Kelly is assigned to red team
        s_chk.add(team[1] != False)
    elif idx == 2:  # Olga is assigned to green team
        s_chk.add(team[4] != True)
    elif idx == 3:  # Lateefah is a facilitator
        s_chk.add(fac[2] != True)
    elif idx == 4:  # Mei is a facilitator
        s_chk.add(fac[3] != True)
    
    # If UNSAT, the choice must be true
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)