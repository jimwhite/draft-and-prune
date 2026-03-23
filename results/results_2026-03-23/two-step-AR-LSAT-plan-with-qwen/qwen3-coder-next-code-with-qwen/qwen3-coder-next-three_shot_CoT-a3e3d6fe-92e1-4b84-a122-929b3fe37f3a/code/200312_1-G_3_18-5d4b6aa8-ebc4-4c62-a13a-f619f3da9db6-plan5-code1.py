from z3 import *

# Cookie types and batch numbers: O1,O2,O3,P1,P2,P3,S1,S2,S3
# Map to indices: 0-8
O1, O2, O3, P1, P2, P3, S1, S2, S3 = range(9)

# Day variables: day[i] is the day (1-5) batch i is made
day = [Int(f"day_{i}") for i in range(9)]

# Base solver
solver = Solver()

# Domain constraints: days 1-5 (Monday-Friday)
for i in range(9):
    solver.add(day[i] >= 1, day[i] <= 5)

# Per-type distinct-day constraints: no two batches of same type on same day
for batch_indices in [[O1, O2, O3], [P1, P2, P3], [S1, S2, S3]]:
    for i in range(3):
        for j in range(i+1, 3):
            solver.add(day[batch_indices[i]] != day[batch_indices[j]])

# Fixed constraints
# At least one batch on Monday (day 1)
solver.add(Or(*[day[i] == 1 for i in range(9)]))

# O2 and P1 on same day
solver.add(day[O2] == day[P1])

# S2 on Thursday (day 4)
solver.add(day[S2] == 4)

# Hypothetical scenario: some first/second/third batch of one type coincides with a third batch of another type
# Create Boolean variables for each (X,Y) pair where X != Y and X's batch k coincides with Y's third batch
exists_pair = {}
for i, (X_type, X_batches) in enumerate([("O", [O1, O2, O3]), ("P", [P1, P2, P3]), ("S", [S1, S2, S3])]):
    for j, (Y_type, Y_batches) in enumerate([("O", [O1, O2, O3]), ("P", [P1, P2, P3]), ("S", [S1, S2, S3])]):
        if X_type != Y_type:
            # For each k in {0,1,2} (batch 1,2,3), check if day[X_batches[k]] == day[Y_batches[2]]
            exists_pair[(X_type, Y_type)] = Or(*[day[X_batches[k]] == day[Y_batches[2]] for k in range(3)])

# Require at least one such pair exists
solver.add(Or(*[exists_pair[(X_type, Y_type)] for (X_type, Y_type) in exists_pair]))

# Answer choices: check which can be false
answer_choices = [
    # 0: "At least one batch of cookies is made on each of the five days."
    lambda d: And(*[Or(*[d[i] == day for i in range(9)]) for day in range(1, 6)]),
    # 1: "At least two batches of cookies are made on Wednesday."
    lambda d: Sum([If(d[i] == 3, 1, 0) for i in range(9)]) >= 2,
    # 2: "Exactly one batch of cookies is made on Monday."
    lambda d: Sum([If(d[i] == 1, 1, 0) for i in range(9)]) == 1,
    # 3: "Exactly two batches of cookies are made on Tuesday."
    lambda d: Sum([If(d[i] == 2, 1, 0) for i in range(9)]) == 2,
    # 4: "Exactly one batch of cookies is made on Friday."
    lambda d: Sum([If(d[i] == 5, 1, 0) for i in range(9)]) == 1
]

answer_index_list = []
for idx, constraint in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert the answer choice is false
    if idx == 0:
        # At least one batch on each day is FALSE → some day has no batches
        s_chk.add(Or(*[And(*[day[i] != day_num for i in range(9)]) for day_num in range(1, 6)]))
    elif idx == 1:
        # At least two batches on Wednesday is FALSE → ≤1 batch on Wednesday (day 3)
        s_chk.add(Sum([If(day[i] == 3, 1, 0) for i in range(9)]) <= 1)
    elif idx == 2:
        # Exactly one batch on Monday is FALSE → either 0 or ≥2 batches
        s_chk.add(Or(Sum([If(day[i] == 1, 1, 0) for i in range(9)]) == 0,
                     Sum([If(day[i] == 1, 1, 0) for i in range(9)]) >= 2))
    elif idx == 3:
        # Exactly two batches on Tuesday is FALSE → ≤1 or ≥3 batches
        s_chk.add(Or(Sum([If(day[i] == 2, 1, 0) for i in range(9)]) <= 1,
                     Sum([If(day[i] == 2, 1, 0) for i in range(9)]) >= 3))
    elif idx == 4:
        # Exactly one batch on Friday is FALSE → ≤0 or ≥2 batches
        s_chk.add(Or(Sum([If(day[i] == 5, 1, 0) for i in range(9)]) == 0,
                     Sum([If(day[i] == 5, 1, 0) for i in range(9)]) >= 2))
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)