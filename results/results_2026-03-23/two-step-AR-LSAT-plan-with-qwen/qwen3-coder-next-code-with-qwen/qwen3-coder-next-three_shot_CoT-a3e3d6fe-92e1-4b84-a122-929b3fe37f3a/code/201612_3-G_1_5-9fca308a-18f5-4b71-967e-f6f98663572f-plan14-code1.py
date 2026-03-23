from z3 import *

# Student indices: Juana=0, Kelly=1, Lateefah=2, Mei=3, Olga=4
students = ["Juana", "Kelly", "Lateefah", "Mei", "Olga"]

# Team variables: team[i] = True if student i is on green team, False for red
team = [Bool(f"team_{i}") for i in range(5)]

# Facilitator variables: fac[i] = True if student i is a facilitator
fac = [Bool(f"fac_{i}") for i in range(5)]

# Base solver
solver = Solver()

# Team-size constraint: green team has exactly 2 members (since Lateefah is fixed to green, and total must be 2 or 3)
# Given that Lateefah is on green, we enforce green team size = 2 (so red has 3)
solver.add(Sum([If(team[i], 1, 0) for i in range(5)]) == 2)

# Given assignments
solver.add(team[2] == True)  # Lateefah is on green team
solver.add(team[0] != team[4])  # Juana and Olga on different teams
solver.add(fac[4] == True)  # Olga is a facilitator

# Team-facilitator constraints: each team has exactly one facilitator
# Green team facilitator count = 1
green_facilitators = [If(And(team[i], fac[i]), 1, 0) for i in range(5)]
solver.add(Sum(green_facilitators) == 1)

# Red team facilitator count = 1
red_facilitators = [If(And(Not(team[i]), fac[i]), 1, 0) for i in range(5)]
solver.add(Sum(red_facilitators) == 1)

# Kelly is not a facilitator
solver.add(fac[1] == False)

# Impose the conditional assumption: Mei is on green team
solver.add(team[3] == True)

# Answer choices (as logical conditions)
answer_conditions = [
    team[0],  # Juana is assigned to the green team
    Not(team[1]),  # Kelly is assigned to the red team (i.e., not on green)
    team[4],  # Olga is assigned to the green team
    fac[2],  # Lateefah is a facilitator
    fac[3]   # Mei is a facilitator
]

# Check each answer choice using proof by contradiction
answer_index_list = []
for idx, cond in enumerate(answer_conditions):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert the negation of the condition
    s_chk.add(Not(cond))
    
    # If UNSAT, then the condition must be true
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)