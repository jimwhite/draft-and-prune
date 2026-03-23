from z3 import *

# Cookie types: 0-oatmeal, 1-peanut butter, 2-sugar
# Days: 1-5 (Monday-Friday)

# Batch day variables: o1,o2,o3 for oatmeal; p1,p2,p3 for peanut butter; s1,s2,s3 for sugar
o1, o2, o3 = Int('o1'), Int('o2'), Int('o3')
p1, p2, p3 = Int('p1'), Int('p2'), Int('p3')
s1, s2, s3 = Int('s1'), Int('s2'), Int('s3')

solver = Solver()

# Domain constraints: each batch day between 1 and 5
for var in [o1, o2, o3, p1, p2, p3, s1, s2, s3]:
    solver.add(var >= 1, var <= 5)

# No two batches of same type on same day (distinct within each type)
solver.add(o1 != o2, o1 != o3, o2 != o3)
solver.add(p1 != p2, p1 != p3, p2 != p3)
solver.add(s1 != s2, s1 != s3, s2 != s3)

# At least one batch on Monday (day 1)
solver.add(Or(o1 == 1, o2 == 1, o3 == 1,
              p1 == 1, p2 == 1, p3 == 1,
              s1 == 1, s2 == 1, s3 == 1))

# Fixed constraints
solver.add(o2 == p1)      # second oatmeal = first peanut butter
solver.add(s2 == 4)       # second sugar on Thursday

# Ordering constraints per type: batches made in order
solver.add(o1 < o2, o2 < o3)
solver.add(p1 < p2, p2 < p3)
solver.add(s1 < s2, s2 < s3)

# Assumption: one kind's first batch same day as another kind's third batch
assumption = Or(
    o1 == p3, o1 == s3,
    p1 == o3, p1 == s3,
    s1 == o3, s1 == p3
)

# Combine base constraints with assumption
base_with_assumption = And(
    And(solver.assertions()),
    assumption
)

# Define helper to count batches on a given day
def count_on_day(day_val):
    return Sum([If(var == day_val, 1, 0) for var in [o1, o2, o3, p1, p2, p3, s1, s2, s3]])

# Answer choices conditions
# 0: At least one batch on each of the five days → all days have count >=1
cond0 = And(count_on_day(1) >= 1, count_on_day(2) >= 1,
            count_on_day(3) >= 1, count_on_day(4) >= 1,
            count_on_day(5) >= 1)

# 1: At least two batches on Wednesday (day 3)
cond1 = count_on_day(3) >= 2

# 2: Exactly one batch on Monday (day 1)
cond2 = count_on_day(1) == 1

# 3: Exactly two batches on Tuesday (day 2)
cond3 = count_on_day(2) == 2

# 4: Exactly one batch on Friday (day 5)
cond4 = count_on_day(5) == 1

# Check each answer choice: find which could be false (i.e., its negation is satisfiable under assumption)
answer_index_list = []
for idx, cond in enumerate([cond0, cond1, cond2, cond3, cond4]):
    s_chk = Solver()
    # Add base_with_assumption
    s_chk.add(base_with_assumption)
    # Add negation of condition
    s_chk.add(Not(cond))
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)