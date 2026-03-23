from z3 import *

# Cookbook indices: K=0, L=1, M=2, N=3, O=4, P=5
season = [Bool(f"season_{i}") for i in range(6)]

solver = Solver()

# M and P cannot be published in the same season
solver.add(season[2] != season[5])

# K and N must be published in the same season
solver.add(season[0] == season[3])

# If K is in fall, O must be in fall
solver.add(Or(Not(season[0]), season[4]))

# If M is in fall, N must be in spring
solver.add(Or(Not(season[2]), Not(season[3])))

# Given: N is published in fall
solver.add(season[3] == True)

# Answer choices (translate to conditions)
answer_conditions = [
    Not(season[0]),  # A. K is published in the spring
    season[1],       # B. L is published in the fall
    season[2],       # C. M is published in the fall
    Not(season[4]),  # D. O is published in the spring
    Not(season[5])   # E. P is published in the spring
]

# Check each answer choice
answer_index_list = []
for idx, cond in enumerate(answer_conditions):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(cond)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)