from z3 import *

# Student indices: 0-Jiang, 1-Kramer, 2-Lopez, 3-Megregian, 4-O'Neill
# Play indices: 0-Sunset, 1-Tamerlane, 2-Undulation

review = [[Bool(f"review_{i}_{p}") for p in range(3)] for i in range(5)]

solver = Solver()

# Non-empty constraint: each student reviews at least one play
for i in range(5):
    solver.add(Or(review[i][0], review[i][1], review[i][2]))

# Kramer and Lopez each review fewer plays than Megregian
k_count = Sum([If(review[1][p], 1, 0) for p in range(3)])
l_count = Sum([If(review[2][p], 1, 0) for p in range(3)])
m_count = Sum([If(review[3][p], 1, 0) for p in range(3)])
solver.add(k_count < m_count)
solver.add(l_count < m_count)

# Neither Lopez nor Megregian reviews any play Jiang reviews
for p in range(3):
    solver.add(Not(And(review[0][p], review[2][p])))
    solver.add(Not(And(review[0][p], review[3][p])))

# Kramer and O'Neill both review Tamerlane
solver.add(review[1][1] == True)
solver.add(review[4][1] == True)

# Exactly two students review exactly the same set of plays
same_pairs = []
for i in range(5):
    for j in range(i+1, 5):
        same_ij = And([
            review[i][0] == review[j][0],
            review[i][1] == review[j][1],
            review[i][2] == review[j][2]
        ])
        same_pairs.append(same_ij)

solver.add(Sum([If(pair, 1, 0) for pair in same_pairs]) == 1)

# Exactly three students review Undulation
solver.add(Sum([If(review[i][2], 1, 0) for i in range(5)]) == 3)

# Check each answer choice
answer_choices = [
    "Megregian does not review Undulation.",  # A: ¬review[3][2]
    "O'Neill does not review Undulation.",   # B: ¬review[4][2]
    "Jiang reviews Undulation.",             # C: review[0][2]
    "Lopez reviews Tamerlane.",              # D: review[2][1]
    "O'Neill reviews Sunset."                # E: review[4][0]
]

answer_index_list = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    if idx == 0:  # Megregian does not review Undulation
        s_chk.add(Not(review[3][2]))
    elif idx == 1:  # O'Neill does not review Undulation
        s_chk.add(Not(review[4][2]))
    elif idx == 2:  # Jiang reviews Undulation
        s_chk.add(review[0][2])
    elif idx == 3:  # Lopez reviews Tamerlane
        s_chk.add(review[2][1])
    elif idx == 4:  # O'Neill reviews Sunset
        s_chk.add(review[4][0])
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)