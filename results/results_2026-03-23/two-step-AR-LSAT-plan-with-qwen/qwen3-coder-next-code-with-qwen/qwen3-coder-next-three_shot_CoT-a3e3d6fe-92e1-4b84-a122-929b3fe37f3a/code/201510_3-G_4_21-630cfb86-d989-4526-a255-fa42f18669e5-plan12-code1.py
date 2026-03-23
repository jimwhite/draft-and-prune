from z3 import *

# Book indices: K=0, L=1, M=2, N=3, O=4, P=5
season = [Bool(f"season_{i}") for i in range(6)]

solver = Solver()

# Base constraints
# M and P cannot be published in the same season
solver.add(season[2] != season[5])

# K and N must be published in the same season
solver.add(season[0] == season[3])

# If K is published in fall, O must be published in fall
solver.add(Implies(season[0], season[4]))

# If M is published in fall, N must be published in spring
solver.add(Implies(season[2], Not(season[3])))

# Given condition: N is published in fall
solver.add(season[3])

# Check each answer choice
answer_choices = [
    "K is published in the spring.",  # season[0] == False
    "L is published in the fall.",     # season[1] == True
    "M is published in the fall.",     # season[2] == True
    "O is published in the spring.",   # season[4] == False
    "P is published in the spring."    # season[5] == False
]

answer_index_list = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add the specific assertion for this choice
    if idx == 0:  # K in spring
        s_chk.add(Not(season[0]))
    elif idx == 1:  # L in fall
        s_chk.add(season[1])
    elif idx == 2:  # M in fall
        s_chk.add(season[2])
    elif idx == 3:  # O in spring
        s_chk.add(Not(season[4]))
    elif idx == 4:  # P in spring
        s_chk.add(Not(season[5]))
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)