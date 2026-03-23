from z3 import *

# Cookie types: 0=OAT, 1=PBU, 2=SUG
# Days: 0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri

# Batch day variables
first_oat = Int('first_oat')
second_oat = Int('second_oat')
third_oat = Int('third_oat')
first_pbu = Int('first_pbu')
second_pbu = Int('second_pbu')
third_pbu = Int('third_pbu')
first_sug = Int('first_sug')
second_sug = Int('second_sug')
third_sug = Int('third_sug')

# Base solver
solver = Solver()

# Domain constraints: each batch day between 0 and 4
for var in [first_oat, second_oat, third_oat,
            first_pbu, second_pbu, third_pbu,
            first_sug, second_sug, third_sug]:
    solver.add(var >= 0, var <= 4)

# Distinct-day-per-type constraints: no two batches of same type on same day
solver.add(first_oat != second_oat, first_oat != third_oat, second_oat != third_oat)
solver.add(first_pbu != second_pbu, first_pbu != third_pbu, second_pbu != third_pbu)
solver.add(first_sug != second_sug, first_sug != third_sug, second_sug != third_sug)

# At least one batch on Monday (day 0)
solver.add(Or(*[var == 0 for var in [
    first_oat, second_oat, third_oat,
    first_pbu, second_pbu, third_pbu,
    first_sug, second_sug, third_sug]]))

# Given constraints
solver.add(second_oat == first_pbu)
solver.add(second_sug == 3)

# Conditional antecedent: there exists a pair of different-type batches where one is first/second/third
# and the other is first/second/third, both on same day.
# We'll encode this using existential quantification with helper variables.

# Create boolean flags for each possible pair
pairs = []
# (type1, batch_idx1, type2, batch_idx2) where type1 != type2
# batch_idx: 0=first, 1=second, 2=third

batch_vars = {
    (0, 0): first_oat, (0, 1): second_oat, (0, 2): third_oat,
    (1, 0): first_pbu, (1, 1): second_pbu, (1, 2): third_pbu,
    (2, 0): first_sug, (2, 1): second_sug, (2, 2): third_sug
}

# Generate all pairs of different types
for t1 in range(3):
    for b1 in range(3):
        for t2 in range(3):
            if t1 == t2:
                continue
            for b2 in range(3):
                pairs.append(((t1, b1), (t2, b2)))

# Create boolean variables to select which pair matches
match_vars = [Bool(f"match_{i}") for i in range(len(pairs))]

# At least one pair must match
solver.add(Or(*match_vars))

# For each match variable, enforce the equality if selected
for i, ((t1, b1), (t2, b2)) in enumerate(pairs):
    solver.add(Implies(match_vars[i], batch_vars[(t1, b1)] == batch_vars[(t2, b2)]))

# Answer choices (statements that could be false)
# A: At least one batch on each day
# B: At least two batches on Wednesday (day 2)
# C: Exactly one batch on Monday
# D: Exactly two batches on Tuesday
# E: Exactly one batch on Friday

def count_batches_on_day(day):
    return Sum([If(var == day, 1, 0) for var in [
        first_oat, second_oat, third_oat,
        first_pbu, second_pbu, third_pbu,
        first_sug, second_sug, third_sug]])

# Check each answer choice (negate to see if it can be false)
answer_index_list = []

# A: At least one batch on each day (negation: some day has no batches)
s_chk_A = Solver()
s_chk_A.add(solver.assertions())
# Negation: exists a day with no batches
days = [0, 1, 2, 3, 4]
neg_A_constraints = []
for d in days:
    day_has_batch = Or(*[var == d for var in [
        first_oat, second_oat, third_oat,
        first_pbu, second_pbu, third_pbu,
        first_sug, second_sug, third_sug]])
    neg_A_constraints.append(Not(day_has_batch))
s_chk_A.add(Or(*neg_A_constraints))

if s_chk_A.check() == sat:
    answer_index_list.append(0)

# B: At least two batches on Wednesday (day 2)
s_chk_B = Solver()
s_chk_B.add(solver.assertions())
# Negation: fewer than 2 batches on Wednesday (0 or 1)
s_chk_B.add(count_batches_on_day(2) < 2)

if s_chk_B.check() == sat:
    answer_index_list.append(1)

# C: Exactly one batch on Monday
s_chk_C = Solver()
s_chk_C.add(solver.assertions())
# Negation: not exactly one batch on Monday (0 or >=2)
s_chk_C.add(count_batches_on_day(0) != 1)

if s_chk_C.check() == sat:
    answer_index_list.append(2)

# D: Exactly two batches on Tuesday
s_chk_D = Solver()
s_chk_D.add(solver.assertions())
# Negation: not exactly two batches on Tuesday
s_chk_D.add(count_batches_on_day(1) != 2)

if s_chk_D.check() == sat:
    answer_index_list.append(3)

# E: Exactly one batch on Friday
s_chk_E = Solver()
s_chk_E.add(solver.assertions())
# Negation: not exactly one batch on Friday
s_chk_E.add(count_batches_on_day(4) != 1)

if s_chk_E.check() == sat:
    answer_index_list.append(4)

print(answer_index_list)