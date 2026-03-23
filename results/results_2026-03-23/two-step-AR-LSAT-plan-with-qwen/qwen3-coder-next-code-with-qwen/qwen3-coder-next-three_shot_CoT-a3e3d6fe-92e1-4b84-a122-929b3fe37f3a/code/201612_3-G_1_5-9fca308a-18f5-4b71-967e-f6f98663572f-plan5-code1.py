from z3 import *

# Student indices: 0=Juana, 1=Kelly, 2=Lateefah, 3=Mei, 4=Olga
students = ["Juana", "Kelly", "Lateefah", "Mei", "Olga"]

# Team assignment variables: green[i] is True if student i is on green team
green = [Bool(f"green_{i}") for i in range(5)]

# Facilitator variables: facilitator[i] is True if student i is a facilitator
facilitator = [Bool(f"facilitator_{i}") for i in range(5)]

# Base solver
solver = Solver()

# Team-size constraint: exactly 2 on one team and 3 on the other
solver.add(Sum([If(green[i], 1, 0) for i in range(5)]) == 2)

# Fixed assignment: Lateefah is on green team
solver.add(green[2] == True)

# Juana and Olga on different teams
solver.add(green[0] != green[4])

# Olga is a facilitator
solver.add(facilitator[4] == True)

# Kelly is not a facilitator
solver.add(facilitator[1] == False)

# Exactly one facilitator per team
# Green team facilitator: exactly one student on green team is a facilitator
green_facilitators = [And(green[i], facilitator[i]) for i in range(5)]
solver.add(Sum([If(f, 1, 0) for f in green_facilitators]) == 1)

# Red team facilitator: exactly one student not on green team is a facilitator
red_facilitators = [And(Not(green[i]), facilitator[i]) for i in range(5)]
solver.add(Sum([If(f, 1, 0) for f in red_facilitators]) == 1)

# Conditional assumption: Mei is assigned to green team
solver.add(green[3] == True)

# Choices (indices correspond to the given options)
choices = [
    "Juana is assigned to the green team.",  # green[0] == True
    "Kelly is assigned to the red team.",   # green[1] == False
    "Olga is assigned to the green team.",  # green[4] == True
    "Lateefah is a facilitator.",           # facilitator[2] == True
    "Mei is a facilitator."                 # facilitator[3] == True
]

# Check each choice using proof by contradiction
answer_index_list = []
for idx, choice in enumerate(choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add the negation of the choice
    if idx == 0:  # Juana is assigned to green team -> negation: green[0] == False
        s_chk.add(green[0] == False)
    elif idx == 1:  # Kelly is assigned to red team -> negation: green[1] == True
        s_chk.add(green[1] == True)
    elif idx == 2:  # Olga is assigned to green team -> negation: green[4] == False
        s_chk.add(green[4] == False)
    elif idx == 3:  # Lateefah is a facilitator -> negation: facilitator[2] == False
        s_chk.add(facilitator[2] == False)
    elif idx == 4:  # Mei is a facilitator -> negation: facilitator[3] == False
        s_chk.add(facilitator[3] == False)
    
    # If UNSAT, the choice must be true
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)