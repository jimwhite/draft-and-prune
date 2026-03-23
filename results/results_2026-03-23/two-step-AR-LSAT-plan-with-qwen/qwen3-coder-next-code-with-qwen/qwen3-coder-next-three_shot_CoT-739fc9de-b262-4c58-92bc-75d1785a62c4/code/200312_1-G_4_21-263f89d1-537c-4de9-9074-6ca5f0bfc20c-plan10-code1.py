from z3 import *

# Student indices: Jiang=0, Kramer=1, Lopez=2, Megregian=3, O'Neill=4
# Play indices: Sunset=0, Tamerlane=1, Undulation=2

review = [[Bool(f"review_{s}_{p}") for p in range(3)] for s in range(5)]

solver = Solver()

# At-least-one-play constraint
for s in range(5):
    solver.add(Or(review[s][0], review[s][1], review[s][2]))

# Count function for number of plays reviewed by a student
def count_plays(s):
    return Sum([If(review[s][p], 1, 0) for p in range(3)])

# Kramer and Lopez each review fewer plays than Megregian
solver.add(count_plays(1) < count_plays(3))
solver.add(count_plays(2) < count_plays(3))

# Lopez and Jiang share no plays
for p in range(3):
    solver.add(Or(Not(review[2][p]), Not(review[0][p])))

# Lopez and Megregian share no plays
for p in range(3):
    solver.add(Or(Not(review[2][p]), Not(review[3][p])))

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

# Exactly one pair has identical review sets
solver.add(Sum([If(sp, 1, 0) for sp in same_pairs]) == 1)

# Exactly three students review Undulation
solver.add(Sum([If(review[s][2], 1, 0) for s in range(5)]) == 3)

# Answer choices (hypotheses to test)
answer_options = [
    Not(review[3][2]),  # Megregian does not review Undulation
    Not(review[4][2]),  # O'Neill does not review Undulation
    review[0][2],       # Jiang reviews Undulation
    review[2][1],       # Lopez reviews Tamerlane
    review[4][0]        # O'Neill reviews Sunset
]

# Check each option
answer_index_list = []
for idx, opt in enumerate(answer_options):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(opt)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)