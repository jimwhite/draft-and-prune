from z3 import *

# Cookbook indices: K=0, L=1, M=2, N=3, O=4, P=5
cookbooks = ["K", "L", "M", "N", "O", "P"]

# Boolean variables: fall[i] = True if cookbook i is published in fall
fall = [Bool(f"fall_{c}") for c in cookbooks]

# Base solver with all constraints
solver = Solver()

# M and P cannot be published in the same season
solver.add(fall[0] != fall[5])  # M and P different seasons

# K and N must be published in the same season
solver.add(fall[0] == fall[3])  # K and N same season

# If K is published in the fall, O must also be published in the fall
solver.add(Implies(fall[0], fall[4]))

# If M is published in the fall, N must be published in the spring
solver.add(Implies(fall[2], Not(fall[3])))

# Given condition: N is published in the fall
solver.add(fall[3])

# Answer choices (indices correspond to positions in the list)
answer_choices = [
    "K is published in the spring.",  # A: Not fall[0]
    "L is published in the fall.",     # B: fall[1]
    "M is published in the fall.",     # C: fall[2]
    "O is published in the spring.",   # D: Not fall[4]
    "P is published in the spring."    # E: Not fall[5]
]

# Check each answer choice
answer_index_list = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add the specific choice condition
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