from z3 import *

# Cookie types: 0-oatmeal, 1-peanut butter, 2-sugar
# Days: Monday=1, Tuesday=2, Wednesday=3, Thursday=4, Friday=5

# Batch positions: o1,o2,o3 for oatmeal; p1,p2,p3 for peanut butter; s1,s2,s3 for sugar
o1, o2, o3 = Int('o1'), Int('o2'), Int('o3')
p1, p2, p3 = Int('p1'), Int('p2'), Int('p3')
s1, s2, s3 = Int('s1'), Int('s2'), Int('s3')

# Base solver
solver = Solver()

# Domain constraints: each batch position between 1 and 5
for var in [o1, o2, o3, p1, p2, p3, s1, s2, s3]:
    solver.add(var >= 1, var <= 5)

# Distinctness per type: batches on different days
solver.add(o1 != o2, o1 != o3, o2 != o3)
solver.add(p1 != p2, p1 != p3, p2 != p3)
solver.add(s1 != s2, s1 != s3, s2 != s3)

# Ordering within type: batches made in sequence
solver.add(o1 < o2, o2 < o3)
solver.add(p1 < p2, p2 < p3)
solver.add(s1 < s2, s2 < s3)

# Fixed constraints
# At least one batch on Monday (day 1)
solver.add(Or(o1 == 1, o2 == 1, o3 == 1, p1 == 1, p2 == 1, p3 == 1, s1 == 1, s2 == 1, s3 == 1))

# Second oatmeal batch coincides with first peanut butter
solver.add(o2 == p1)

# Second sugar batch on Thursday (day 4)
solver.add(s2 == 4)

# Premise: one kind's first batch same day as another kind's third batch
premise = Or(
    o1 == s3,  # oatmeal first = sugar third
    p1 == o3,  # peanut butter first = oatmeal third
    s1 == o3,  # sugar first = oatmeal third
    o1 == p3,  # oatmeal first = peanut butter third
    p1 == s3,  # peanut butter first = sugar third
    s1 == p3   # sugar first = peanut butter third
)

# Answer choices (as logical statements about daily batch counts)
# We'll compute counts for each day and check the negation of each statement

def count_on_day(day_val):
    return Sum([If(var == day_val, 1, 0) for var in [o1, o2, o3, p1, p2, p3, s1, s2, s3]])

# A: At least one batch on each of the five days
# Negation: some day has 0 batches
A_neg = Or(
    count_on_day(1) == 0,
    count_on_day(2) == 0,
    count_on_day(3) == 0,
    count_on_day(4) == 0,
    count_on_day(5) == 0
)

# B: At least two batches on Wednesday (day 3)
# Negation: fewer than 2 batches on Wednesday
B_neg = count_on_day(3) < 2

# C: Exactly one batch on Monday (day 1)
# Negation: not exactly one batch on Monday
C_neg = count_on_day(1) != 1

# D: Exactly two batches on Tuesday (day 2)
# Negation: not exactly two batches on Tuesday
D_neg = count_on_day(2) != 2

# E: Exactly one batch on Friday (day 5)
# Negation: not exactly one batch on Friday
E_neg = count_on_day(5) != 1

# Check each answer choice (find which could be false under the premise)
answer_index_list = []

# For A
s_chk = Solver()
s_chk.add(solver.assertions())
s_chk.add(premise)
s_chk.add(A_neg)
if s_chk.check() == sat:
    answer_index_list.append(0)

# For B
s_chk = Solver()
s_chk.add(solver.assertions())
s_chk.add(premise)
s_chk.add(B_neg)
if s_chk.check() == sat:
    answer_index_list.append(1)

# For C
s_chk = Solver()
s_chk.add(solver.assertions())
s_chk.add(premise)
s_chk.add(C_neg)
if s_chk.check() == sat:
    answer_index_list.append(2)

# For D
s_chk = Solver()
s_chk.add(solver.assertions())
s_chk.add(premise)
s_chk.add(D_neg)
if s_chk.check() == sat:
    answer_index_list.append(3)

# For E
s_chk = Solver()
s_chk.add(solver.assertions())
s_chk.add(premise)
s_chk.add(E_neg)
if s_chk.check() == sat:
    answer_index_list.append(4)

print(answer_index_list)