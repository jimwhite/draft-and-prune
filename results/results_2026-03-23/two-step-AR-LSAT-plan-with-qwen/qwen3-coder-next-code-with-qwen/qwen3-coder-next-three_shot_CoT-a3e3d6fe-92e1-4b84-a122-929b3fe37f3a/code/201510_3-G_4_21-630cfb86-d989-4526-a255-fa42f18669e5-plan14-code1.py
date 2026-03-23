from z3 import *

# Cookbook indices: K=0, L=1, M=2, N=3, O=4, P=5
fall = [Bool(f"fall_{i}") for i in range(6)]

# Base solver
solver = Solver()

# M and P cannot be published in the same season
solver.add(fall[2] != fall[5])

# K and N must be published in the same season
solver.add(fall[0] == fall[3])

# If K is published in the fall, O must also be published in the fall
solver.add(Or(Not(fall[0]), fall[4]))

# If M is published in the fall, N must be published in the spring
solver.add(Or(Not(fall[2]), Not(fall[3])))

# Given condition: N is published in the fall
solver.add(fall[3])

# Check each answer choice
answer_choices = [
    "K is published in the spring.",  # ~fall[0]
    "L is published in the fall.",     # fall[1]
    "M is published in the fall.",     # fall[2]
    "O is published in the spring.",   # ~fall[4]
    "P is published in the spring."    # ~fall[5]
]

answer_index_list = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add the specific condition for this choice
    if idx == 0:  # K is published in the spring
        s_chk.add(Not(fall[0]))
    elif idx == 1:  # L is published in the fall
        s_chk.add(fall[1])
    elif idx == 2:  # M is published in the fall
        s_chk.add(fall[2])
    elif idx == 3:  # O is published in the spring
        s_chk.add(Not(fall[4]))
    elif idx == 4:  # P is published in the spring
        s_chk.add(Not(fall[5]))
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)