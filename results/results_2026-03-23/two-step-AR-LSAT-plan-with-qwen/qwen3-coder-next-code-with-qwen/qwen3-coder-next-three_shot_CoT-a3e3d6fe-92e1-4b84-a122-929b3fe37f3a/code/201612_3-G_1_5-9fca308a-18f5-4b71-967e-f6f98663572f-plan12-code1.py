from z3 import *

# Students: Juana=0, Kelly=1, Lateefah=2, Mei=3, Olga=4
team = [Int(f"team_{i}") for i in range(5)]
facilitator = [Bool(f"facilitator_{i}") for i in range(5)]

solver = Solver()

# Team assignment: 0=green, 1=red
for i in range(5):
    solver.add(Or(team[i] == 0, team[i] == 1))

# Given constraints
solver.add(team[2] == 0)  # Lateefah is on green team
solver.add(team[3] == 0)  # Mei is on green team (conditional premise)
solver.add(team[0] != team[4])  # Juana and Olga on different teams
solver.add(facilitator[4] == True)  # Olga is a facilitator
solver.add(facilitator[1] == False)  # Kelly is not a facilitator

# Team size constraint: one team has 2 members, the other has 3
green_count = Sum([If(team[i] == 0, 1, 0) for i in range(5)])
solver.add(Or(green_count == 2, green_count == 3))

# Exactly one facilitator per team
solver.add(
    Sum([If(team[i] == 0, If(facilitator[i], 1, 0), 0) for i in range(5)]) == 1
)
solver.add(
    Sum([If(team[i] == 1, If(facilitator[i], 1, 0), 0) for i in range(5)]) == 1
)

# Answer choices (as conditions)
answer_conditions = [
    team[0] == 0,           # Juana is assigned to the green team
    team[1] == 1,           # Kelly is assigned to the red team
    team[4] == 0,           # Olga is assigned to the green team
    facilitator[2] == True, # Lateefah is a facilitator
    facilitator[3] == True  # Mei is a facilitator
]

answer_index_list = []
for idx, cond in enumerate(answer_conditions):
    s_chk = Solver()
    for a in solver.assertions():
        s_chk.add(a)
    
    # Check if negation is satisfiable
    s_chk.add(Not(cond))
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)