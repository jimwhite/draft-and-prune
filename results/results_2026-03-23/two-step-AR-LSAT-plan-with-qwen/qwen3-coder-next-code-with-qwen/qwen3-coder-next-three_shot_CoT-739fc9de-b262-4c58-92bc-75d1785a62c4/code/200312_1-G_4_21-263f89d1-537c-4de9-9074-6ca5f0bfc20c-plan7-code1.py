from z3 import *

# Student indices: Jiang=0, Kramer=1, Lopez=2, Megregian=3, O'Neill=4
# Play indices: Sunset=0, Tamerlane=1, Undulation=2

review = [[Bool(f"review_{i}_{p}") for p in range(3)] for i in range(5)]

solver = Solver()

# Non-empty review constraint: each student reviews at least one play
for i in range(5):
    solver.add(Or(review[i][0], review[i][1], review[i][2]))

# Kramer and Lopez each review fewer plays than Megregian
count = lambda i: Sum([If(review[i][p], 1, 0) for p in range(3)])
solver.add(count(1) < count(3))
solver.add(count(2) < count(3))

# Lopez and Megregian do not review any play Jiang reviews
for p in range(3):
    solver.add(Implies(review[0][p], Not(review[2][p])))
    solver.add(Implies(review[0][p], Not(review[3][p])))

# Kramer and O'Neill both review Tamerlane
solver.add(review[1][1] == True)
solver.add(review[4][1] == True)

# Exactly two students have identical review sets
identical = []
for i in range(5):
    for j in range(i+1, 5):
        identical_ij = And(
            review[i][0] == review[j][0],
            review[i][1] == review[j][1],
            review[i][2] == review[j][2]
        )
        identical.append(identical_ij)

# Exactly one pair has identical review sets
solver.add(Sum([If(id, 1, 0) for id in identical]) == 1)

# Exactly three students review Undulation
solver.add(Sum([If(review[i][2], 1, 0) for i in range(5)]) == 3)

# Answer choices conditions
answer_conditions = [
    Not(review[3][2]),           # Choice 0: Megregian does not review Undulation
    Not(review[4][2]),           # Choice 1: O'Neill does not review Undulation
    review[0][2],                # Choice 2: Jiang reviews Undulation
    review[2][1],                # Choice 3: Lopez reviews Tamerlane
    review[4][0]                 # Choice 4: O'Neill reviews Sunset
]

# Check each answer choice
answer_index_list = []
for k in range(5):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(answer_conditions[k])
    
    if s_chk.check() == sat:
        answer_index_list.append(k)

print(answer_index_list)