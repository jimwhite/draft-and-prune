from z3 import *

# Student indices: Jiang=0, Kramer=1, Lopez=2, Megregian=3, O'Neill=4
# Play indices: Sunset=0, Tamerlane=1, Undulation=2

review = [[Bool(f"review_{i}_{p}") for p in range(3)] for i in range(5)]

solver = Solver()

# At-least-one-play constraint
for i in range(5):
    solver.add(Or(review[i][0], review[i][1], review[i][2]))

# Count function for number of plays reviewed by student i
def count_plays(i):
    return Sum([If(review[i][p], 1, 0) for p in range(3)])

# Kramer and Lopez each review fewer plays than Megregian
solver.add(count_plays(1) < count_plays(3))
solver.add(count_plays(2) < count_plays(3))

# Neither Lopez nor Megregian reviews any play Jiang reviews
for p in range(3):
    solver.add(Implies(review[2][p], Not(review[0][p])))  # Lopez
    solver.add(Implies(review[3][p], Not(review[0][p])))  # Megregian

# Kramer and O'Neill both review Tamerlane
solver.add(review[1][1] == True)
solver.add(review[4][1] == True)

# Exactly two students review exactly the same set of plays
same_pairs = []
for i in range(5):
    for j in range(i+1, 5):
        same_ij = And(
            review[i][0] == review[j][0],
            review[i][1] == review[j][1],
            review[i][2] == review[j][2]
        )
        same_pairs.append(same_ij)

# Exactly one pair has identical review sets
solver.add(Sum([If(pair, 1, 0) for pair in same_pairs]) == 1)

# Exactly three students review Undulation
solver.add(Sum([If(review[i][2], 1, 0) for i in range(5)]) == 3)

# Answer choices conditions
answer_conditions = [
    Not(review[3][2]),      # Megregian does not review Undulation
    Not(review[4][2]),      # O'Neill does not review Undulation
    review[0][2],           # Jiang reviews Undulation
    review[2][1],           # Lopez reviews Tamerlane
    review[4][0]            # O'Neill reviews Sunset
]

answer_index_list = []
for idx, cond in enumerate(answer_conditions):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(cond)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)