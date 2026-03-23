from z3 import *

# Student indices: 0=Jiang, 1=Kramer, 2=Lopez, 3=Megregian, 4=O'Neill
# Play indices: 0=Sunset, 1=Tamerlane, 2=Undulation

review = [[Bool(f"review_{i}_{j}") for j in range(3)] for i in range(5)]

solver = Solver()

# Nonempty constraint: each student reviews at least one play
for i in range(5):
    solver.add(Or(review[i][0], review[i][1], review[i][2]))

# Helper function to count how many plays a student reviews
def count_reviews(i):
    return Sum([If(review[i][j], 1, 0) for j in range(3)])

# Kramer and Lopez each review fewer plays than Megregian
solver.add(count_reviews(1) < count_reviews(3))
solver.add(count_reviews(2) < count_reviews(3))

# Lopez and Megregian review no play Jiang reviews
for j in range(3):
    solver.add(Not(And(review[0][j], review[2][j])))
    solver.add(Not(And(review[0][j], review[3][j])))

# Kramer and O'Neill both review Tamerlane
solver.add(review[1][1] == True)
solver.add(review[4][1] == True)

# Exactly two students review exactly the same set of plays
# Enumerate all 7 nonempty subsets of {0,1,2}
subsets = []
for mask in range(1, 8):  # 001 to 111
    subset = []
    for j in range(3):
        if mask & (1 << j):
            subset.append(j)
    subsets.append(subset)

# For each student and subset, define whether the student reviews exactly that subset
same_subset = [[None for _ in range(len(subsets))] for _ in range(5)]
for i in range(5):
    for idx, subset in enumerate(subsets):
        # Student i reviews exactly the plays in this subset
        conds = []
        for j in range(3):
            if j in subset:
                conds.append(review[i][j])
            else:
                conds.append(Not(review[i][j]))
        same_subset[i][idx] = And(*conds)

# Exactly one subset has exactly two students, all others have at most one
subset_counts = []
for idx in range(len(subsets)):
    count = Sum([If(same_subset[i][idx], 1, 0) for i in range(5)])
    subset_counts.append(count)

# Exactly one subset has count == 2, all others have count <= 1
exactly_one_double = []
for idx in range(len(subsets)):
    other_constraints = [subset_counts[j] <= 1 for j in range(len(subsets)) if j != idx]
    other_constraints.append(subset_counts[idx] == 2)
    exactly_one_double.append(And(*other_constraints))

solver.add(Or(*exactly_one_double))

# Exactly three students review Undulation (play index 2)
solver.add(Sum([If(review[i][2], 1, 0) for i in range(5)]) == 3)

# Answer choices
answer_choices = [
    lambda: Not(review[3][2]),  # Megregian does not review Undulation
    lambda: Not(review[4][2]),  # O'Neill does not review Undulation
    lambda: review[0][2] == True,  # Jiang reviews Undulation
    lambda: review[2][1] == True,  # Lopez reviews Tamerlane
    lambda: review[4][0] == True   # O'Neill reviews Sunset
]

answer_index_list = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(choice())
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)