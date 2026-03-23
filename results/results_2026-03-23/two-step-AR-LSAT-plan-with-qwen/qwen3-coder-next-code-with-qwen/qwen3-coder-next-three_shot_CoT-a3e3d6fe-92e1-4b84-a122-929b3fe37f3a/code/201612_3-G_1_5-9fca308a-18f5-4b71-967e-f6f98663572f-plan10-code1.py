from z3 import *

# Student indices: Juana=0, Kelly=1, Lateefah=2, Mei=3, Olga=4
students = 5

# Team variables: team[i] = 0 for green, 1 for red
team = [Int(f"team_{i}") for i in range(students)]

# Facilitator variables
facilitator = [Bool(f"fac_{i}") for i in range(students)]

# Base solver
solver = Solver()

# Team size constraints: one team has 2 members, the other has 3
green_count = Sum([If(team[i] == 0, 1, 0) for i in range(students)])
solver.add(Or(green_count == 2, green_count == 3))

# Exactly one facilitator per team
green_facilitators = Sum([If(team[i] == 0, If(facilitator[i], 1, 0), 0) for i in range(students)])
red_facilitators = Sum([If(team[i] == 1, If(facilitator[i], 1, 0), 0) for i in range(students)])
solver.add(green_facilitators == 1)
solver.add(red_facilitators == 1)

# Given constraints
# Juana and Olga on different teams
solver.add(team[0] != team[4])
# Lateefah on green team
solver.add(team[2] == 0)
# Kelly is not a facilitator
solver.add(Not(facilitator[1]))
# Olga is a facilitator
solver.add(facilitator[4] == True)

# Hypothetical condition: Mei is on green team
solver.add(team[3] == 0)

# Answer choices (indices correspond to the given list)
answer_choices = [
    "Juana is assigned to the green team.",      # 0: team[0] == 0
    "Kelly is assigned to the red team.",        # 1: team[1] == 1
    "Olga is assigned to the green team.",       # 2: team[4] == 0
    "Lateefah is a facilitator.",                # 3: facilitator[2] == True
    "Mei is a facilitator."                      # 4: facilitator[3] == True
]

# Check each answer choice for necessity (must be true in all satisfying assignments)
answer_index_list = []
for idx, condition_desc in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert the negation of the condition
    if idx == 0:  # Juana on green team (team[0] == 0)
        s_chk.add(team[0] != 0)
    elif idx == 1:  # Kelly on red team (team[1] == 1)
        s_chk.add(team[1] != 1)
    elif idx == 2:  # Olga on green team (team[4] == 0)
        s_chk.add(team[4] != 0)
    elif idx == 3:  # Lateefah is facilitator (facilitator[2] == True)
        s_chk.add(Not(facilitator[2]))
    elif idx == 4:  # Mei is facilitator (facilitator[3] == True)
        s_chk.add(Not(facilitator[3]))
    
    # If UNSAT, the condition must be true
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

# Output the single correct index
print(answer_index_list[0] if answer_index_list else -1)