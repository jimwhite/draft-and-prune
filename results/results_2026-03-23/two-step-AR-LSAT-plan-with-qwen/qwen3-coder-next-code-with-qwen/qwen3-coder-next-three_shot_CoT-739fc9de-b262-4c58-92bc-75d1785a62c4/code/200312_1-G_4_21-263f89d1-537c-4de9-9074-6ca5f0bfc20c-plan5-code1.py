from z3 import *

# Student indices: Jiang=0, Kramer=1, Lopez=2, Megregian=3, O'Neill=4
# Play indices: Sunset=0, Tamerlane=1, Undulation=2

review = [[Bool(f"review_{i}_{p}") for p in range(3)] for i in range(5)]

solver = Solver()

# At-least-one constraint: each student reviews at least one play
for i in range(5):
    solver.add(Or(review[i][0], review[i][1], review[i][2]))

# Kramer and Lopez each review fewer plays than Megregian
count = lambda idx: Sum([If(review[idx][p], 1, 0) for p in range(3)])
solver.add(count(1) < count(3))  # Kramer < Megregian
solver.add(count(2) < count(3))  # Lopez < Megregian

# Neither Lopez nor Megregian reviews any play Jiang reviews
for p in range(3):
    solver.add(Implies(review[0][p], And(Not(review[2][p]), Not(review[3][p]))))

# Kramer and O'Neill both review Tamerlane
solver.add(review[1][1] == True)
solver.add(review[4][1] == True)

# Exactly two students review exactly the same set of plays
# We need to enforce that there is exactly one pair (i,j) with i<j such that
# for all p, review[i][p] == review[j][p], and no other pairs have this property

# First, define equality between students
eq = [[Bool(f"eq_{i}_{j}") for j in range(5)] for i in range(5)]
for i in range(5):
    for j in range(i+1, 5):
        solver.add(eq[i][j] == And(review[i][0] == review[j][0],
                                   review[i][1] == review[j][1],
                                   review[i][2] == review[j][2]))

# Count the number of equal pairs
equal_pairs = []
for i in range(5):
    for j in range(i+1, 5):
        equal_pairs.append(eq[i][j])

solver.add(Sum([If(pair, 1, 0) for pair in equal_pairs]) == 1)

# Exactly three students review Undulation (play index 2)
solver.add(Sum([If(review[i][2], 1, 0) for i in range(5)]) == 3)

# Answer choices
answer_choices = [
    Not(review[3][2]),      # Megregian does not review Undulation
    Not(review[4][2]),      # O'Neill does not review Undulation
    review[0][2],           # Jiang reviews Undulation
    review[2][1],           # Lopez reviews Tamerlane
    review[4][0]            # O'Neill reviews Sunset
]

answer_index_list = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(choice)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)