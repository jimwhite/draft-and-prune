from z3 import *

# Student indices: 0=Jiang, 1=Kramer, 2=Lopez, 3=Megregian, 4=O'Neill
# Play indices: 0=Sunset, 1=Tamerlane, 2=Undulation

review = [[Bool(f"review_{i}_{j}") for j in range(3)] for i in range(5)]

solver = Solver()

# At-least-one constraint: each student reviews at least one play
for i in range(5):
    solver.add(Or(review[i][0], review[i][1], review[i][2]))

# Kramer and Lopez each review fewer plays than Megregian
count = lambda idx: Sum([If(review[idx][j], 1, 0) for j in range(3)])
solver.add(count(1) < count(3))  # Kramer < Megregian
solver.add(count(2) < count(3))  # Lopez < Megregian

# Neither Lopez nor Megregian reviews any play Jiang reviews
for j in range(3):
    solver.add(Implies(review[2][j], Not(review[0][j])))  # Lopez -> not Jiang
    solver.add(Implies(review[3][j], Not(review[0][j])))  # Megregian -> not Jiang

# Kramer and O'Neill both review Tamerlane
solver.add(review[1][1] == True)
solver.add(review[4][1] == True)

# Exactly two students review exactly the same set of plays
# We need to express: there is exactly one pair (i,j) with i<j such that they have identical reviews
# and all other pairs are different

# First, create equality constraints for each pair
equal_pairs = []
for i in range(5):
    for j in range(i+1, 5):
        eq = And(review[i][0] == review[j][0],
                 review[i][1] == review[j][1],
                 review[i][2] == review[j][2])
        equal_pairs.append((i, j, eq))

# Exactly one pair is equal
exactly_one_equal = []
for idx in range(len(equal_pairs)):
    # This pair is equal, all others are not
    other_unequal = []
    for jdx in range(len(equal_pairs)):
        if idx != jdx:
            i1, j1, _ = equal_pairs[jdx]
            other_unequal.append(Not(equal_pairs[jdx][2]))
    exactly_one_equal.append(And(equal_pairs[idx][2], *other_unequal))

solver.add(Or(*exactly_one_equal))

# Exactly three students review Undulation
solver.add(Sum([If(review[i][2], 1, 0) for i in range(5)]) == 3)

# Answer choices
answer_choices = [
    ("Megregian does not review Undulation.", Not(review[3][2])),
    ("O'Neill does not review Undulation.", Not(review[4][2])),
    ("Jiang reviews Undulation.", review[0][2]),
    ("Lopez reviews Tamerlane.", review[2][1]),
    ("O'Neill reviews Sunset.", review[4][0])
]

answer_index_list = []
for idx, (desc, constraint) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(constraint)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)