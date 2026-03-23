from z3 import *

# Student indices: 0-Jiang, 1-Kramer, 2-Lopez, 3-Megregian, 4-O'Neill
(J, K, L, M, O) = range(5)

# Play indices: 0-Sunset, 1-Tamerlane, 2-Undulation
(SUN, TAM, UND) = range(3)

# review[i][j] is True if student i reviews play j
review = [[Bool(f"review_{i}_{j}") for j in range(3)] for i in range(5)]

# Base solver
solver = Solver()

# At-least-one-play constraint: each student reviews at least one play
for i in range(5):
    solver.add(Or(review[i][0], review[i][1], review[i][2]))

# Kramer and Lopez each review fewer plays than Megregian
def count_reviews(student):
    return Sum([If(review[student][j], 1, 0) for j in range(3)])

solver.add(count_reviews(K) < count_reviews(M))
solver.add(count_reviews(L) < count_reviews(M))

# Jiang-Lopez/Megregian disjointness constraint
for j in range(3):
    solver.add(Implies(review[J][j], Not(review[L][j])))
    solver.add(Implies(review[J][j], Not(review[M][j])))

# Kramer and O'Neill both review Tamerlane
solver.add(review[K][1] == True)
solver.add(review[O][1] == True)

# Exactly two students review exactly the same plays
# Create pairwise equality indicators
pairwise_equal = []
for i in range(5):
    for j in range(i+1, 5):
        eq = Bool(f"eq_{i}_{j}")
        # eq is True iff students i and j have identical review sets
        solver.add(Implies(eq, And(review[i][0] == review[j][0], 
                                   review[i][1] == review[j][1],
                                   review[i][2] == review[j][2])))
        solver.add(Implies(Not(eq), Or(review[i][0] != review[j][0],
                                       review[i][1] != review[j][1],
                                       review[i][2] != review[j][2])))
        pairwise_equal.append((i, j, eq))

# Exactly one pair has identical review sets
solver.add(Sum([If(eq, 1, 0) for (_, _, eq) in pairwise_equal]) == 1)

# Exactly three students review Undulation
solver.add(Sum([If(review[i][2], 1, 0) for i in range(5)]) == 3)

# Answer choices
answer_choices = [
    ("Megregian does not review Undulation", Not(review[M][2])),
    ("O'Neill does not review Undulation", Not(review[O][2])),
    ("Jiang reviews Undulation", review[J][2]),
    ("Lopez reviews Tamerlane", review[L][1]),
    ("O'Neill reviews Sunset", review[O][0])
]

# Check each answer choice
answer_index_list = []
for idx, (desc, constraint) in enumerate(answer_choices):
    s_chk = Solver()
    # Add all base constraints
    for a in solver.assertions():
        s_chk.add(a)
    # Add the answer choice constraint
    s_chk.add(constraint)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)