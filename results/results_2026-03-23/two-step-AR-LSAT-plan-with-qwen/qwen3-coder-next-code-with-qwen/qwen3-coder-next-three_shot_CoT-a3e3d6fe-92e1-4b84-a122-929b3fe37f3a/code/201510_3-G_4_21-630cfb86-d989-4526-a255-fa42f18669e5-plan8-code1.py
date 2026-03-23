from z3 import *

# Cookbook indices: K=0, L=1, M=2, N=3, O=4, P=5
cookbooks = ["K", "L", "M", "N", "O", "P"]
fall = [Bool(f"fall_{c}") for c in cookbooks]

solver = Solver()

# M and P cannot be published in the same season
solver.add(fall[2] != fall[5])

# K and N must be published in the same season
solver.add(fall[0] == fall[3])

# If K is in fall, then O must be in fall
solver.add(Or(Not(fall[0]), fall[4]))

# If M is in fall, then N must be in spring
solver.add(Or(Not(fall[2]), Not(fall[3])))

# Given: N is published in fall
solver.add(fall[3] == True)

# Answer choices (indices correspond to the list order)
answer_choices = [
    "K is published in the spring.",  # fall[0] == False
    "L is published in the fall.",     # fall[1] == True
    "M is published in the fall.",     # fall[2] == True
    "O is published in the spring.",   # fall[4] == False
    "P is published in the spring."    # fall[5] == False
]

answer_index_list = []

for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add the specific condition for this choice
    if idx == 0:  # K in spring
        s_chk.add(Not(fall[0]))
    elif idx == 1:  # L in fall
        s_chk.add(fall[1])
    elif idx == 2:  # M in fall
        s_chk.add(fall[2])
    elif idx == 3:  # O in spring
        s_chk.add(Not(fall[4]))
    elif idx == 4:  # P in spring
        s_chk.add(Not(fall[5]))
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)