from z3 import *

# Student indices: Juana=0, Kelly=1, Lateefah=2, Mei=3, Olga=4
team = [Bool(f"team_{i}") for i in range(5)]
facilitator = [Bool(f"facilitator_{i}") for i in range(5)]

# Base solver
solver = Solver()

# Team-size constraint: exactly 2 on one team, 3 on the other
g = Sum([If(team[i], 1, 0) for i in range(5)])
solver.add(Or(g == 2, g == 3))

# Fixed constraints
solver.add(team[2] == True)  # Lateefah is on green team
solver.add(facilitator[4] == True)  # Olga is a facilitator
solver.add(facilitator[1] == False)  # Kelly is not a facilitator
solver.add(team[0] != team[4])  # Juana and Olga on different teams

# Facilitator exclusivity: exactly one facilitator per team
green_facilitators = Sum([If(And(team[i], facilitator[i]), 1, 0) for i in range(5)])
red_facilitators = Sum([If(And(Not(team[i]), facilitator[i]), 1, 0) for i in range(5)])
solver.add(green_facilitators == 1)
solver.add(red_facilitators == 1)

# Add condition: Mei is assigned to green team
solver.add(team[3] == True)

# Answer choices (conditions that must be true)
answer_conditions = [
    team[0] == True,  # Juana is assigned to the green team
    team[1] == False,  # Kelly is assigned to the red team
    team[4] == True,  # Olga is assigned to the green team
    facilitator[2] == True,  # Lateefah is a facilitator
    facilitator[3] == True   # Mei is a facilitator
]

# Check which condition must be true (negation leads to UNSAT)
answer_index_list = []
for idx, cond in enumerate(answer_conditions):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    # Add negation of the condition
    s_chk.add(Not(cond))
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

# Print the first (and only) index that must be true
print(answer_index_list[0] if answer_index_list else -1)