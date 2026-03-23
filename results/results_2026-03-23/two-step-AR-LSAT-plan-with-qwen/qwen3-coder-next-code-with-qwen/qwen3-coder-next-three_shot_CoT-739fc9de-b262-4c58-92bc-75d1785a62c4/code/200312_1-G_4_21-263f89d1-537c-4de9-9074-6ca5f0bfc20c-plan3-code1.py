from z3 import *

# Student indices: 0=Jiang, 1=Kramer, 2=Lopez, 3=Megregian, 4=O'Neill
# Play indices: 0=Sunset, 1=Tamerlane, 2=Undulation

review = [[Bool(f"review_{i}_{p}") for p in range(3)] for i in range(5)]

solver = Solver()

# Non-empty review constraint: each student reviews at least one play
for i in range(5):
    solver.add(Or(review[i][0], review[i][1], review[i][2]))

# Kramer and Lopez each review fewer plays than Megregian
def count_reviews(student):
    return Sum([If(review[student][p], 1, 0) for p in range(3)])

solver.add(count_reviews(1) < count_reviews(3))  # Kramer < Megregian
solver.add(count_reviews(2) < count_reviews(3))  # Lopez < Megregian

# Lopez and Jiang share no plays
for p in range(3):
    solver.add(Implies(review[2][p], Not(review[0][p])))

# Megregian and Jiang share no plays
for p in range(3):
    solver.add(Implies(review[3][p], Not(review[0][p])))

# Kramer and O'Neill both review Tamerlane
solver.add(review[1][1] == True)
solver.add(review[4][1] == True)

# Exactly two students review the exact same set of plays (exactly one pair is identical)
eq_pairs = []
for i in range(5):
    for j in range(i+1, 5):
        eq = And(
            review[i][0] == review[j][0],
            review[i][1] == review[j][1],
            review[i][2] == review[j][2]
        )
        eq_pairs.append(eq)

# Exactly one pair is identical
solver.add(Sum([If(eq, 1, 0) for eq in eq_pairs]) == 1)

# Exactly three students review Undulation
solver.add(Sum([If(review[i][2], 1, 0) for i in range(5)]) == 3)

# Answer choices
answer_choices = [
    lambda: Not(review[3][2]),  # Megregian does not review Undulation
    lambda: Not(review[4][2]),  # O'Neill does not review Undulation
    lambda: review[0][2],       # Jiang reviews Undulation
    lambda: review[2][1],       # Lopez reviews Tamerlane
    lambda: review[4][0]        # O'Neill reviews Sunset
]

answer_index_list = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(choice())
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)