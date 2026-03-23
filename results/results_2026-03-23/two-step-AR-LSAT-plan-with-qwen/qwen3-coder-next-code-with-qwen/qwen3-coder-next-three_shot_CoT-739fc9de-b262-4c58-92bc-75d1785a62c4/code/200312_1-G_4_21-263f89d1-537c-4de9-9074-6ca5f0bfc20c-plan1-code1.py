from z3 import *

# Student indices: Jiang=0, Kramer=1, Lopez=2, Megregian=3, O'Neill=4
# Play indices: Sunset=0, Tamerlane=1, Undulation=2

review = [[Bool(f"review_{i}_{p}") for p in range(3)] for i in range(5)]

solver = Solver()

# Non-empty constraint: each student reviews at least one play
for i in range(5):
    solver.add(Or(review[i][0], review[i][1], review[i][2]))

# Kramer and Lopez each review fewer plays than Megregian
count = lambda idx: Sum([If(review[idx][p], 1, 0) for p in range(3)])
solver.add(count(1) < count(3))  # Kramer < Megregian
solver.add(count(2) < count(3))  # Lopez < Megregian

# Neither Lopez nor Megregian reviews any play Jiang reviews
for p in range(3):
    solver.add(Implies(review[2][p], Not(review[0][p])))  # Lopez -> not Jiang
    solver.add(Implies(review[3][p], Not(review[0][p])))  # Megregian -> not Jiang

# Kramer and O'Neill both review Tamerlane
solver.add(review[1][1] == True)
solver.add(review[4][1] == True)

# Exactly two students review exactly the same plays (exactly one duplicate pair)
# We need to count pairs with identical review sets
pairs = []
for i in range(5):
    for j in range(i+1, 5):
        # Create a boolean indicating if students i and j have identical review sets
        same = And([review[i][p] == review[j][p] for p in range(3)])
        pairs.append(same)

# Exactly one pair has identical review sets
solver.add(Sum([If(p, 1, 0) for p in pairs]) == 1)

# Exactly three students review Undulation
solver.add(Sum([If(review[i][2], 1, 0) for i in range(5)]) == 3)

# Answer choices
answer_conditions = [
    Not(review[3][2]),      # Megregian does not review Undulation
    Not(review[4][2]),      # O'Neill does not review Undulation
    review[0][2],           # Jiang reviews Undulation
    review[2][1],           # Lopez reviews Tamerlane
    review[4][0]            # O'Neill reviews Sunset
]

# Check each option
answer_index_list = []
for idx, cond in enumerate(answer_conditions):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(cond)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

# Since the question asks "which one could be true", we return the first SAT option
if answer_index_list:
    print(answer_index_list[0])
else:
    print(-1)