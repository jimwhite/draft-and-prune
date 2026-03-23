from z3 import *

# Student indices: Juana=0, Kelly=1, Lateefah=2, Mei=3, Olga=4
students = ["Juana", "Kelly", "Lateefah", "Mei", "Olga"]
n = 5

# Boolean variables for team assignment: True = green, False = red
team = [Bool(f"team_{i}") for i in range(n)]

# Boolean variables for facilitator assignment
facilitator = [Bool(f"facilitator_{i}") for i in range(n)]

# Base solver
solver = Solver()

# Team-size constraints: one team has 2 members, the other has 3
team_sum = Sum([If(team[i], 1, 0) for i in range(n)])
solver.add(Or(team_sum == 2, team_sum == 3))

# Fixed assignment constraints
solver.add(team[2] == True)  # Lateefah is on green team
solver.add(team[0] != team[4])  # Juana and Olga on different teams
solver.add(facilitator[4] == True)  # Olga is a facilitator
solver.add(facilitator[1] == False)  # Kelly is not a facilitator

# Exactly one facilitator per team
# For green team (team[i] == True), exactly one facilitator
green_facilitators = [And(team[i], facilitator[i]) for i in range(n)]
solver.add(Sum([If(f, 1, 0) for f in green_facilitators]) == 1)

# For red team (team[i] == False), exactly one facilitator
red_facilitators = [And(Not(team[i]), facilitator[i]) for i in range(n)]
solver.add(Sum([If(f, 1, 0) for f in red_facilitators]) == 1)

# Given conditional assumption: Mei is assigned to green team
solver.add(team[3] == True)

# Answer choices (indices correspond to the order in the problem)
answer_choices = [
    "Juana is assigned to the green team.",  # team[0] == True
    "Kelly is assigned to the red team.",    # team[1] == False
    "Olga is assigned to the green team.",   # team[4] == True
    "Lateefah is a facilitator.",            # facilitator[2] == True
    "Mei is a facilitator."                  # facilitator[3] == True
]

# Check each answer choice using proof by contradiction
answer_index_list = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert the negation of the answer choice
    if idx == 0:  # Juana is assigned to green team -> negation: team[0] == False
        s_chk.add(team[0] == False)
    elif idx == 1:  # Kelly is assigned to red team -> negation: team[1] == True
        s_chk.add(team[1] == True)
    elif idx == 2:  # Olga is assigned to green team -> negation: team[4] == False
        s_chk.add(team[4] == False)
    elif idx == 3:  # Lateefah is a facilitator -> negation: facilitator[2] == False
        s_chk.add(facilitator[2] == False)
    elif idx == 4:  # Mei is a facilitator -> negation: facilitator[3] == False
        s_chk.add(facilitator[3] == False)
    
    # If UNSAT, the choice must be true
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)