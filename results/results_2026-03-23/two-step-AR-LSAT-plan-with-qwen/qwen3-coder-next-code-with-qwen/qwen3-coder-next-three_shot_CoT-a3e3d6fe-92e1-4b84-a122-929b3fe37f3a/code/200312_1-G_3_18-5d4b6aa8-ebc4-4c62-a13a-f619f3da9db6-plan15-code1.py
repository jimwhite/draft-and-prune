from z3 import *

# Cookie types: 0=oatmeal, 1=peanut butter, 2=sugar
# Days: 0=Monday, 1=Tuesday, 2=Wednesday, 3=Thursday, 4=Friday

# Variables: first[c], second[c], third[c] for c in {0,1,2}
first = [Int(f"first_{c}") for c in range(3)]
second = [Int(f"second_{c}") for c in range(3)]
third = [Int(f"third_{c}") for c in range(3)]

# Base solver
solver = Solver()

# Domain constraints: all batch days between 0 and 4
for c in range(3):
    solver.add(first[c] >= 0, first[c] <= 4)
    solver.add(second[c] >= 0, second[c] <= 4)
    solver.add(third[c] >= 0, third[c] <= 4)

# Strictly increasing days per cookie type
for c in range(3):
    solver.add(first[c] < second[c], second[c] < third[c])

# Fixed constraints
solver.add(second[2] == 3)  # sugar second batch is Thursday (index 3)
solver.add(second[0] == first[1])  # oatmeal second batch same day as peanut butter first batch

# At least one batch on Monday (day 0)
solver.add(Or(
    first[0] == 0, second[0] == 0, third[0] == 0,
    first[1] == 0, second[1] == 0, third[1] == 0,
    first[2] == 0, second[2] == 0, third[2] == 0
))

# Conditional scenario: first batch of one type same day as third batch of another type
solver.add(Or(
    first[0] == third[1], first[0] == third[2],
    first[1] == third[0], first[1] == third[2],
    first[2] == third[0], first[2] == third[1]
))

# Helper function to count batches on a specific day
def count_batches_on_day(day_val):
    return Sum([
        If(first[0] == day_val, 1, 0), If(second[0] == day_val, 1, 0), If(third[0] == day_val, 1, 0),
        If(first[1] == day_val, 1, 0), If(second[1] == day_val, 1, 0), If(third[1] == day_val, 1, 0),
        If(first[2] == day_val, 1, 0), If(second[2] == day_val, 1, 0), If(third[2] == day_val, 1, 0)
    ])

# Answer choices (A-E) as conditions:
# A: At least one batch on each day
# B: At least two batches on Wednesday (day 3)
# C: Exactly one batch on Monday (day 0)
# D: Exactly two batches on Tuesday (day 1)
# E: Exactly one batch on Friday (day 4)

answer_index_list = []

# Check each choice to see if it could be false under the scenario
for idx, condition in enumerate([
    # A: At least one batch on each day (negation: some day has no batches)
    lambda s: Or(
        And(first[0] != 0, second[0] != 0, third[0] != 0,
            first[1] != 0, second[1] != 0, third[1] != 0,
            first[2] != 0, second[2] != 0, third[2] != 0),
        And(first[0] != 1, second[0] != 1, third[0] != 1,
            first[1] != 1, second[1] != 1, third[1] != 1,
            first[2] != 1, second[2] != 1, third[2] != 1),
        And(first[0] != 2, second[0] != 2, third[0] != 2,
            first[1] != 2, second[1] != 2, third[1] != 2,
            first[2] != 2, second[2] != 2, third[2] != 2),
        And(first[0] != 3, second[0] != 3, third[0] != 3,
            first[1] != 3, second[1] != 3, third[1] != 3,
            first[2] != 3, second[2] != 3, third[2] != 3),
        And(first[0] != 4, second[0] != 4, third[0] != 4,
            first[1] != 4, second[1] != 4, third[1] != 4,
            first[2] != 4, second[2] != 4, third[2] != 4)
    ),
    # B: At least two batches on Wednesday (day 3) → negation: fewer than 2
    lambda s: count_batches_on_day(3) < 2,
    # C: Exactly one batch on Monday (day 0) → negation: not exactly 1
    lambda s: count_batches_on_day(0) != 1,
    # D: Exactly two batches on Tuesday (day 1) → negation: not exactly 2
    lambda s: count_batches_on_day(1) != 2,
    # E: Exactly one batch on Friday (day 4) → negation: not exactly 1
    lambda s: count_batches_on_day(4) != 1
]):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add negation of the condition
    s_chk.add(condition(s_chk))
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)