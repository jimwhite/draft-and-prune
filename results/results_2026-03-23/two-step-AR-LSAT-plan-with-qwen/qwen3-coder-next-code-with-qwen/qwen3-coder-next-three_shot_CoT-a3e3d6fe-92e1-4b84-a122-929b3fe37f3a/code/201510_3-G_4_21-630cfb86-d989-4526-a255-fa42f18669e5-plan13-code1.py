from z3 import *

# Cookbook indices: K=0, L=1, M=2, N=3, O=4, P=5
cookbooks = ["K", "L", "M", "N", "O", "P"]

# Boolean variables: fall[i] = True if cookbook i is published in fall
fall = [Bool(f"fall_{c}") for c in cookbooks]

# Base solver
solver = Solver()

# M and P cannot be published in the same season: fall[M] != fall[P]
solver.add(fall[2] != fall[5])

# K and N must be published in the same season: fall[K] == fall[N]
solver.add(fall[0] == fall[3])

# If K is published in the fall, O must also be published in the fall: not fall[K] or fall[O]
solver.add(Or(Not(fall[0]), fall[4]))

# If M is published in the fall, N must be published in the spring: not fall[M] or not fall[N]
solver.add(Or(Not(fall[2]), Not(fall[3])))

# Given assumption: N is published in the fall
solver.add(fall[3] == True)

# Answer choices (indices correspond to positions in the list)
answer_choices = [
    "K is published in the spring.",  # A: not fall[0]
    "L is published in the fall.",     # B: fall[1]
    "M is published in the fall.",     # C: fall[2]
    "O is published in the spring.",   # D: not fall[4]
    "P is published in the spring."    # E: not fall[5]
]

# Check each answer choice
answer_index_list = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add the specific constraint for this choice
    if idx == 0:  # K in spring: not fall[0]
        s_chk.add(Not(fall[0]))
    elif idx == 1:  # L in fall: fall[1]
        s_chk.add(fall[1])
    elif idx == 2:  # M in fall: fall[2]
        s_chk.add(fall[2])
    elif idx == 3:  # O in spring: not fall[4]
        s_chk.add(Not(fall[4]))
    elif idx == 4:  # P in spring: not fall[5]
        s_chk.add(Not(fall[5]))
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)