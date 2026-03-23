from z3 import *

# Student indices: 0-Juana, 1-Kelly, 2-Lateefah, 3-Mei, 4-Olga
students = ["Juana", "Kelly", "Lateefah", "Mei", "Olga"]

# Boolean variables: team[i] = True if student i is on green team
team = [Bool(f"team_{i}") for i in range(5)]

# Boolean variables: fac[i] = True if student i is facilitator
fac = [Bool(f"fac_{i}") for i in range(5)]

# Base solver
solver = Solver()

# Team-size constraints: one team has 2 members, the other has 3
# Since Lateefah and Mei are on green (fixed), green must have exactly 2 members
solver.add(Sum([If(team[i], 1, 0) for i in range(5)]) == 2)

# Fixed constraints
solver.add(team[2] == True)  # Lateefah on green
solver.add(team[3] == True)  # Mei on green (assumption)
solver.add(team[0] != team[4])  # Juana and Olga on different teams
solver.add(fac[4] == True)  # Olga is a facilitator

# Facilitator constraints: exactly one per team
# Each student can only be facilitator if on the team they belong to
green_fac_sum = Sum([If(And(team[i], fac[i]), 1, 0) for i in range(5)])
red_fac_sum = Sum([If(And(Not(team[i]), fac[i]), 1, 0) for i in range(5)])
solver.add(green_fac_sum == 1)
solver.add(red_fac_sum == 1)

# Kelly not facilitator
solver.add(fac[1] == False)

# Answer choices (as logical expressions)
answer_choices = [
    team[0] == True,  # Juana on green
    team[1] == False,  # Kelly on red
    team[4] == True,  # Olga on green
    fac[2] == True,  # Lateefah is facilitator
    fac[3] == True   # Mei is facilitator
]

# Check each answer choice: must it be true in all models?
answer_index_list = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert the negation of the choice
    s_chk.add(Not(choice))
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)