from z3 import *

# Cookbook indices: K=0, L=1, M=2, N=3, O=4, P=5
cookbooks = ["K", "L", "M", "N", "O", "P"]

# Boolean variables: fall[i] is True if cookbook i is published in fall
fall = [Bool(f"fall_{c}") for c in cookbooks]

# Base solver
solver = Solver()

# Constraints:
# M and P cannot be published in the same season
solver.add(fall[2] != fall[5])

# K and N must be published in the same season
solver.add(fall[0] == fall[3])

# If K is published in the fall, O must also be published in the fall
solver.add(Implies(fall[0], fall[4]))

# If M is published in the fall, N must be published in the spring
solver.add(Implies(fall[2], Not(fall[3])))

# Additional assumption: N is published in the fall
solver.add(fall[3] == True)

# Answer choices (indices correspond to positions in the list)
answer_choices = [
    Not(fall[0]),  # K is published in the spring
    fall[1],       # L is published in the fall
    fall[2],       # M is published in the fall
    Not(fall[4]),  # O is published in the spring
    Not(fall[5])   # P is published in the spring
]

# Check each answer choice
answer_index_list = []
for idx, cond in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(cond)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)