from z3 import *

# Student indices: Jiang=0, Kramer=1, Lopez=2, Megregian=3, O'Neill=4
# Play indices: Sunset=0, Tamerlane=1, Undulation=2

review = [[Bool(f"review_{s}_{p}") for p in range(3)] for s in range(5)]

solver = Solver()

# Non-empty review constraint: each student reviews at least one play
for s in range(5):
    solver.add(Or(review[s][0], review[s][1], review[s][2]))

# Kramer and Lopez review fewer plays than Megregian
def count_reviews(student):
    return Sum([If(review[student][p], 1, 0) for p in range(3)])

solver.add(count_reviews(1) < count_reviews(3))  # Kramer < Megregian
solver.add(count_reviews(2) < count_reviews(3))  # Lopez < Megregian

# Neither Lopez nor Megregian reviews any play Jiang reviews
for p in range(3):
    solver.add(Implies(review[2][p], Not(review[0][p])))  # Lopez => not Jiang
    solver.add(Implies(review[3][p], Not(review[0][p])))  # Megregian => not Jiang

# Kramer and O'Neill both review Tamerlane
solver.add(review[1][1] == True)  # Kramer reviews Tamerlane
solver.add(review[4][1] == True)  # O'Neill reviews Tamerlane

# Exactly two students have identical review sets
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
solver.add(Sum([If(review[s][2], 1, 0) for s in range(5)]) == 3)

# Answer choices
answer_choices = [
    Not(review[3][2]),      # A) Megregian does not review Undulation
    Not(review[4][2]),      # B) O'Neill does not review Undulation
    review[0][2],           # C) Jiang reviews Undulation
    review[2][1],           # D) Lopez reviews Tamerlane
    review[4][0]            # E) O'Neill reviews Sunset
]

# Check each choice
valid_indices = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(choice)
    
    if s_chk.check() == sat:
        valid_indices.append(idx)

print(valid_indices)